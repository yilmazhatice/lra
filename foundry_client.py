"""Foundry Local'in yerel HTTP sunucusuna baglanma ve model yonetimi.

Foundry Local her baslatildiginda farkli bir port kullanabiliyor ve modelleri
bellekten atabiliyor (bilgisayar yeniden basladiginda, sunucu kapandiginda).
Uygulama kodu bunlarla ugrasmasin diye hepsi burada toplaniyor:

- Adres her kullanimdan once canli mi diye kontrol edilir; oluyse sunucu
  baslatilip adres yeniden okunur.
- Model istekten once bellege yuklenir.
- Istek yine de "yuklu degil" hatasi alirsa model yeniden yuklenir ve istek
  bir kez tekrarlanir.
- set_primary() ile tanimlanan model bellege her zaman ilk yuklenir ve
  isitilir (ayrinti set_primary'de).

Kullanim:
    resp = with_model("qwen2.5-7b", lambda model_id:
        client().chat.completions.create(model=model_id, ...))
"""

import json
import os
import subprocess
import time

import openai
import requests
from openai import OpenAI

_endpoint = None
_client = None
_models = None      # sunucunun listeledigi (indirilmis) model id'leri
_loaded = set()     # bellekte oldugunu dogruladigimiz model id'leri
_primary = None     # (alias, isitma_fonksiyonu): bellege ilk girecek model
_warmed = False     # birincil model bu sunucuda sirasiyla yuklenip isitildi mi

# Isitma istemi sinirlari. Olcum (qwen2.5-7b, RTX 5070 8 GB): temiz bellekte
# ilk token ~0.7-1.4 sn ve ~44 token/sn; bozuk bellekte ilk token 1.7-17 sn
# ya da uretim ~21 token/sn.
WARMUP_TOKENS = 24
SLOW_TTFT_SEC = 3.0
MIN_TOKENS_PER_SEC = 30.0


def _foundry(*args, timeout=60):
    """foundry CLI komutunu JSON ciktiyla calistirip sonucu dondur."""
    try:
        out = subprocess.run(
            ["foundry", *args, "--output", "json"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=timeout,
        )
    except FileNotFoundError:
        raise RuntimeError(
            "'foundry' komutu bulunamadi. Foundry Local kurulu mu? "
            "Windows: winget install Microsoft.FoundryLocal"
        ) from None

    if out.returncode != 0:
        try:
            detay = json.loads(out.stderr)["error"]["message"]
        except (ValueError, KeyError, TypeError):
            detay = (out.stderr or out.stdout).strip()
        raise RuntimeError(f"'foundry {' '.join(args)}' basarisiz: {detay}")

    return json.loads(out.stdout) if out.stdout.strip() else {}


def _detect_endpoint():
    """Sunucu adresini ortam degiskeninden ya da sunucuyu baslatarak oku.

    'foundry server start' sunucu zaten calisiyorsa da adresi dondurur.
    """
    if os.environ.get("FOUNDRY_ENDPOINT"):
        return os.environ["FOUNDRY_ENDPOINT"].rstrip("/")

    urls = _foundry("server", "start", timeout=120).get("webUrls") or []
    if not urls:
        raise RuntimeError(
            "Foundry sunucusunun adresi bulunamadi. "
            "Terminalde 'foundry server start' calistirip tekrar deneyin."
        )
    return urls[0].rstrip("/")


def _alive(endpoint):
    try:
        requests.get(endpoint + "/v1/models", timeout=5).raise_for_status()
        return True
    except Exception:
        return False


def get_endpoint():
    """Calisan sunucunun adresi. Onbellekteki adres oluyse yeniden bulunur."""
    global _endpoint, _client, _models, _warmed

    if _endpoint and _alive(_endpoint):
        return _endpoint

    _endpoint = _detect_endpoint()

    if not _alive(_endpoint):
        # Foundry CLI bazen calismayan bir sunucuyu "zaten calisiyor" diye
        # bildiriyor ve olu bir adres donuyor. Servisi durdurup yeniden
        # baslatiyor, adresi tekrar okuyoruz.
        subprocess.run(
            ["foundry", "server", "stop"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=60,
        )
        _endpoint = _detect_endpoint()

    if not _alive(_endpoint):
        raise RuntimeError(
            f"Foundry sunucusuna ulasilamiyor: {_endpoint}. "
            "Terminalde 'foundry server stop' ve 'foundry server start' deneyin."
        )

    # Yeni sunucu: adrese ve bellek durumuna bagli onbellekleri sifirla
    _client = None
    _models = None
    _loaded.clear()
    _warmed = False
    return _endpoint


def base_url():
    return get_endpoint() + "/v1"


def client():
    """Guncel adrese bagli OpenAI istemcisi."""
    global _client
    url = base_url()
    if _client is None or str(_client.base_url).rstrip("/") != url:
        _client = OpenAI(base_url=url, api_key="not-needed")
    return _client


def _loaded_models():
    """Su anda bellekte olan modellerin id'leri (surum eki olmadan)."""
    return {
        m["displayName"]
        for m in _foundry("cache", "list").get("models", [])
        if m.get("loaded")
    }


def find_model(alias):
    """Indirilmis modeller icinde adinda alias gecen model id'sini dondur.

    Birden fazla eslesme varsa (ornegin ayni modelin GPU ve NPU surumu)
    bellekte olan tercih edilir. Modelin bellekte oldugunu garanti etmez;
    istek atmak icin with_model() kullanin.
    """
    global _models

    if _models is None:
        resp = requests.get(base_url() + "/models", timeout=30)
        resp.raise_for_status()
        _models = [m["id"] for m in resp.json().get("data", [])]

    matches = [m for m in _models if alias.lower() in m.lower()]
    if not matches:
        raise RuntimeError(
            f"'{alias}' modeli indirilmemis. "
            f"'foundry model info {alias}' ile surumlerine bakip "
            "cihaziniza uygun olani 'foundry model download <surum>' ile indirin."
        )
    if len(matches) > 1:
        loaded = _loaded_models()
        matches.sort(key=lambda m: m not in loaded)
    return matches[0]


def ensure_loaded(model_id):
    """Model bellekte degilse yukle. Tam surum adiyla yuklenir; alias ile
    yuklemek cihaza uymayan bir surumu secebiliyor."""
    if model_id in _loaded:
        return
    if model_id not in _loaded_models():
        _foundry("model", "load", model_id, timeout=600)
    _loaded.add(model_id)


def set_primary(alias, warmup_messages):
    """Bellege her zaman ilk yuklenecek modeli ve isitma istemini tanimla.

    8 GB'lik kartta sohbet ve gomme modeli birlikte bellegin sinirinda. Bellek
    dolunca surucu yeni ayirmalari hata vermeden sistem RAM'ine yonlendiriyor
    ve o bellegi kullanan adim cok yavasliyor. Sohbet modeli agirliklarini ve
    baglam okuma icin gereken calisma bellegini gomme modelinden once ayirirsa
    yanit ~2.5 sn, ters sirada ~50 sn suruyor. Model bellekten bosaltilip
    yeniden yuklenmesi yetmiyor (uretim hizi yariya dusuyor); temiz bir sunucu
    gerekiyor (olcumler: muhammet_ws/olcum_betikleri/hiz_*.py).

    warmup_messages() uygulamanin gonderebilecegi en uzun istemi dondurmeli;
    calisma bellegi o boyuta gore ayriliyor.
    """
    global _primary, _warmed
    _primary = (alias, warmup_messages)
    _warmed = False


def _warm(model_id, messages):
    """Istemi gonder; (ilk token suresi, uretim hizi token/sn) dondur."""
    started = time.perf_counter()
    first = None
    tokens = 0
    stream = client().chat.completions.create(
        model=model_id, messages=messages, temperature=0.0,
        max_tokens=WARMUP_TOKENS, stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            first = first or time.perf_counter()
            tokens += 1
    end = time.perf_counter()
    if first is None:
        return end - started, None
    # Ilk token'dan sonraki sure yalnizca uretimi olcer
    rate = (tokens - 1) / (end - first) if tokens > 5 else None
    return first - started, rate


def _ensure_primary():
    """Birincil modeli bu sunucuda bir kez, temiz bellekte ilk sirada yukle."""
    global _warmed
    if _primary is None or _warmed:
        return
    alias, warmup_messages = _primary
    primary = find_model(alias)
    loaded = _loaded_models()
    messages = warmup_messages()

    # Sunucu uygulamadan bagimsiz calistigi icin modeller onceki bir
    # calismadan, bilinmeyen bir duzende yuklu kalmis olabilir. Isitma
    # istemi hizliysa bellek duzeni saglam demektir.
    if primary in loaded:
        ttft, rate = _warm(primary, messages)
        if ttft < SLOW_TTFT_SEC and (rate is None or rate >= MIN_TOKENS_PER_SEC):
            _loaded.update(loaded)
            _warmed = True
            return

    if loaded:
        # Bosaltilan modelin bellegi karta tam geri donmuyor; sunucuyu
        # yeniden baslatmak gerekiyor. get_endpoint() sunucuyu yeniden
        # baslatip onbellekleri sifirlar.
        subprocess.run(
            ["foundry", "server", "stop"],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=120,
        )
        get_endpoint()
        primary = find_model(alias)

    _foundry("model", "load", primary, timeout=600)
    _warm(primary, messages)
    _loaded.add(primary)
    _warmed = True


def with_model(alias, request):
    """request(model_id) cagrisini model bellekte olacak sekilde calistir.

    Model iki istek arasinda bellekten atilmis olabilir; o durumda gelen
    "not loaded" hatasinda model yeniden yuklenir ve istek bir kez tekrarlanir.
    """
    global _warmed
    _ensure_primary()
    model_id = find_model(alias)
    ensure_loaded(model_id)
    try:
        return request(model_id)
    except openai.BadRequestError as err:
        if "not loaded" not in str(err).lower():
            raise
        _loaded.discard(model_id)
        if _primary and model_id == find_model(_primary[0]):
            _warmed = False
            _ensure_primary()
        ensure_loaded(model_id)
        return request(model_id)

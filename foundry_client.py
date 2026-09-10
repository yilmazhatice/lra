"""Foundry Local'in yerel HTTP sunucusuna baglanma yardimcilari.

Foundry Local her baslatildiginda farkli bir port kullanabiliyor. Bu yuzden
adresi bir kez bulup sonsuza kadar saklamiyoruz; her kullanimdan once canli
mi diye bakiyor, olu ise yeniden tespit ediyoruz.
"""

import os
import re
import subprocess

import requests
from openai import OpenAI

_endpoint = None
_client = None
_models = None


def _detect_endpoint():
    """Sunucu adresini ortam degiskeninden ya da CLI ciktisindan oku."""
    if os.environ.get("FOUNDRY_ENDPOINT"):
        return os.environ["FOUNDRY_ENDPOINT"].rstrip("/")

    out = subprocess.run(
        ["foundry", "server", "start"],
        capture_output=True,
        text=True,
        timeout=120,
    )
    match = re.search(r"https?://[\d.]+:\d+", out.stdout + out.stderr)
    if not match:
        raise RuntimeError(
            "Foundry sunucusunun adresi bulunamadi. "
            "Terminalde 'foundry server start' calistirip tekrar deneyin."
        )
    return match.group(0)


def _alive(endpoint):
    try:
        requests.get(endpoint + "/v1/models", timeout=5).raise_for_status()
        return True
    except Exception:
        return False


def get_endpoint():
    """Calisan sunucunun adresi. Onbellekteki adres oluyse yeniden bulunur."""
    global _endpoint, _client, _models

    if _endpoint and _alive(_endpoint):
        return _endpoint

    _endpoint = _detect_endpoint()

    if not _alive(_endpoint):
        # Foundry CLI bazen calismayan bir sunucuyu "zaten calisiyor" diye
        # bildiriyor ve olu bir adres donuyor. Servisi durdurup yeniden
        # baslatiyor, adresi tekrar okuyoruz.
        subprocess.run(
            ["foundry", "server", "stop"],
            capture_output=True, text=True, timeout=60,
        )
        _endpoint = _detect_endpoint()

    if not _alive(_endpoint):
        raise RuntimeError(
            f"Foundry sunucusuna ulasilamiyor: {_endpoint}. "
            "Terminalde 'foundry server stop' ve 'foundry server start' deneyin."
        )

    # Adres degismis olabilir; adrese bagli onbellekleri sifirla
    _client = None
    _models = None
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


def find_model(alias):
    """Sunucudaki modeller icinde alias gecen ilkini dondur.

    Model henuz bellege yuklenmemisse bir kez yuklemeyi dener.
    """
    global _models

    for deneme in (1, 2):
        if _models is None:
            resp = requests.get(base_url() + "/models", timeout=30)
            resp.raise_for_status()
            _models = [m["id"] for m in resp.json().get("data", [])]

        for model_id in _models:
            if alias.lower() in model_id.lower():
                return model_id

        if deneme == 1:
            subprocess.run(
                ["foundry", "model", "load", alias],
                capture_output=True, text=True, timeout=600,
            )
            _models = None
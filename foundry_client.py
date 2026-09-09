"""Foundry Local'in yerel HTTP sunucusuna baglanma yardimcilari."""

import os
import re
import functools
import subprocess

import requests


@functools.lru_cache(maxsize=1)
def get_endpoint():
    """Foundry Local sunucusunun adresini bul.

    Port makineye gore degistigi icin sabit yazmiyoruz. `foundry server
    start` komutu sunucu zaten calisiyorsa onu yeniden baslatmaz, sadece
    adresi bildirir; biz de o ciktidan okuyoruz.
    """
    if os.environ.get("FOUNDRY_ENDPOINT"):
        return os.environ["FOUNDRY_ENDPOINT"].rstrip("/")

    out = subprocess.run(
        ["foundry", "server", "start"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    match = re.search(r"https?://[\d.]+:\d+", out.stdout + out.stderr)
    if not match:
        raise RuntimeError(
            "Foundry sunucusunun adresi bulunamadi. "
            "'foundry server start' komutunu elle calistirin."
        )
    return match.group(0)


def base_url():
    return get_endpoint() + "/v1"


@functools.lru_cache(maxsize=8)
def find_model(keyword):
    """Sunucudaki modeller arasindan adinda keyword gecen ilkini dondur."""
    resp = requests.get(base_url() + "/models", timeout=30)
    resp.raise_for_status()
    ids = [m["id"] for m in resp.json().get("data", [])]
    for model_id in ids:
        if keyword.lower() in model_id.lower():
            return model_id
    raise RuntimeError(f"'{keyword}' iceren model yok. Mevcut: {ids}")
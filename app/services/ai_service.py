import logging
import requests
from flask import current_app

loglayici = logging.getLogger(__name__)

class YapayZekaServisi:
    def yanit_uret(self, kullanici_mesaji: str, sohbet_gecmisi: list = None) -> str:
        return self._gemini_cagir(kullanici_mesaji, sohbet_gecmisi or [])

    def _sistem_talimati_olustur(self) -> str:
        # 'BUSINESS_CONTEXT' arıyoruz
        return current_app.config.get(
            "BUSINESS_CONTEXT",
            "Sen yardımcı bir iş asistanısın."
        )

    def _gemini_cagir(self, kullanici_mesaji: str, gecmis: list) -> str:
        api_anahtari = current_app.config.get("GEMINI_API_KEY", "")

        if not api_anahtari:
            loglayici.warning("GEMINI_API_KEY ayarlanmamış! Demo modu devrede.")
            return self._demo_yaniti_ver(kullanici_mesaji)

        baglanti_adresi = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent"
        
        
        istek_basliklari = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_anahtari,
        }
            

        sistem_talimati = self._sistem_talimati_olustur()
        icerik_paketi = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in gecmis]
        icerik_paketi.append({"role": "user", "parts": [{"text": f"{sistem_talimati}\n\nKullanıcı: {kullanici_mesaji}"}]})

        gonderilecek_veri = {
            "contents": icerik_paketi,
            "generationConfig": { "temperature": 0.7, "maxOutputTokens": 500, "topP": 0.95 }
        }

        try:
            sunucu_cevabi = requests.post(baglanti_adresi, json=gonderilecek_veri, timeout=15, headers=istek_basliklari)
            sunucu_cevabi.raise_for_status()
            gelen_veri = sunucu_cevabi.json()
            uretilen_metin = gelen_veri["candidates"][0]["content"]["parts"][0]["text"]
            return uretilen_metin.strip()
        except Exception as hata:
            loglayici.error(f"Gemini Hatası: {hata}")
            raise YapayZekaServisHatasi("Yapay zekâ servisine ulaşılamadı.")

    def _demo_yaniti_ver(self, kullanici_mesaji: str) -> str:
        return "Sistem API anahtarı bulunamadığı için demo modunda çalışıyor. Lütfen .env dosyanızı kontrol ediniz."

class YapayZekaServisHatasi(Exception):
    pass

yapay_zeka_servisi = YapayZekaServisi()


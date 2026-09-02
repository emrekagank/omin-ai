import logging
import requests
from flask import current_app

logger = logging.getLogger(__name__)

class AIService:
    def response(self, usr_msg: str, chat_hist: list = None) -> str:
        return self._gemini_cagir(usr_msg, chat_hist or [])

    def _system_prompt(self) -> str:

        return current_app.config.get(
            "BUSINESS_CONTEXT",
            "Sen yardımcı bir iş asistanısın."
        )

    def _gemini_cagir(self, usr_msg: str, chat_hist: list) -> str:
        api_anahtari = current_app.config.get("GEMINI_API_KEY", "")

        if not api_anahtari:
            logger.warning("GEMINI_API_KEY ayarlanmamış! Demo modu devrede.")
            return self._demo_yaniti_ver(usr_msg)

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent"
        
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_anahtari,
        }
            

        sys_prompt = self._system_prompt()
        content = [{"role": m["role"], "parts": [{"text": m["content"]}]} for m in chat_hist]
        content.append({"role": "user", "parts": [{"text": f"{sys_prompt}\n\nKullanıcı: {usr_msg}"}]})

        user_prompt = {
            "contents": content,
            "generationConfig": { "temperature": 0.7, "maxOutputTokens": 512, "topP": 0.95 }
        }

        try:
            ai_answer = requests.post(url, json=user_prompt, timeout=15, headers=headers)
            ai_answer.raise_for_status()
            answer = ai_answer.json()
            generated_text = answer["candidates"][0]["content"]["parts"][0]["text"]
            return generated_text.strip()
        except Exception as hata:
            logger.error(f"Gemini Hatası: {hata}")
            raise YapayZekaServisHatasi("Yapay zekâ servisine ulaşılamadı.")

    def _demo_yaniti_ver(self, kullanici_mesaji: str) -> str:
        return "Sistem API anahtarı bulunamadığı için demo modunda çalışıyor. Lütfen .env dosyanızı kontrol ediniz."

class YapayZekaServisHatasi(Exception):
    pass

yapay_zeka_servisi = AIService()


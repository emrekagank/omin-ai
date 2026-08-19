import os
from dotenv import load_dotenv

load_dotenv()

class CONF:
    # Flask ve Veritabanı (İngilizce standart anahtarlar)
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DATABASE_URL = os.environ.get("DATABASE_URL", "contact_form_register.db")
    
    # API Anahtarları (.env dosyasında tam olarak böyle yazmalı)
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")
    
    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        "Rolün: Sen TechDrone Systems firmasının resmi B2B yapay zekâ satış asistanısın. "
        "Firma Bilgisi: Savunma, lojistik ve tarım sektörlerine yönelik otonom insansız "
        "hava araçları (drone) ve yapay zekâ destekli izleme sistemleri üretiyoruz. "
        "KURALLAR: "
        "1. Her zaman birinci çoğul şahıs kullan ('Biz', 'Firmamız', 'TechDrone Systems olarak'). "
        "2. Kesinlikle 'Sen TechDrone Systems olarak' gibi hatalı cümleler kurma. "
        "3. Kullanıcıya her zaman kibar, kurumsal ve profesyonel bir destek botu gibi yaklaş. "
        "4. Yanıtların kısa, net ve tamamen Türkçe olsun. "
        "5. Müşterinin ihtiyacını anladıktan sonra onu iletişim bilgilerini bırakıp demo talep etmeye yönlendir."
    )
    CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

class DevConf(CONF):
    DEBUG = True

class ProConf(CONF):
    DEBUG = False

config_selector = {
    "development": DevConf,
    "production": ProConf,
}
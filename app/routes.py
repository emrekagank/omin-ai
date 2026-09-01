from flask import Blueprint, request, jsonify, render_template
from app.services.ai_service import yapay_zeka_servisi, YapayZekaServisHatasi
from app.database import musteri_adayi_ekle, tum_adaylari_getir

# Rotaları gruplandırmak için Blueprint (Taslak) nesneleri oluşturuyoruz.
api_arayuzu = Blueprint("api", __name__)
sayfa_arayuzu = Blueprint("sayfalar", __name__)

# ─── API UÇ NOKTALARI (Endpoints) ──────────────────────

@api_arayuzu.route("/sohbet", methods=["POST"])
def sohbet_et():
    """
    Ön yüzden gelen sohbet mesajını alır, yapay zeka servisine iletir
    ve üretilen yanıtı JSON formatında ön yüze geri döndürür.
    """
    veri = request.json
    mesaj = veri.get("mesaj")
    gecmis = veri.get("gecmis", [])

    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj alanı boş bırakılamaz."}), 400

    try:
        yanit = yapay_zeka_servisi.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "cevap": yanit})
    except YapayZekaServisHatasi as e:
        return jsonify({"basari": False, "hata": str(e)}), 503

@api_arayuzu.route("/adaylar", methods=["POST"])
def aday_kaydet():
    """
    Ziyaretçinin iletişim formundan gönderdiği isim ve telefon bilgilerini
    alır ve veritabanı katmanını kullanarak kaydeder.
    """
    veri = request.json
    isim = veri.get("isim")
    mail = veri.get("telefon")
    mesaj = veri.get("mesaj")

    if not isim or not mail:
        return jsonify({"basari": False, "hata": "İsim ve mail bilgisi zorunludur."}), 400

    musteri_adayi_ekle(isim, mail, mesaj)
    return jsonify({"basari": True, "mesaj": "Bilgileriniz başarıyla sistemimize kaydedildi."})

@api_arayuzu.route("/adaylar", methods=["GET"])
def adaylari_listele():
    """
    Yönetim panelindeki tabloyu doldurmak için veritabanındaki 
    tüm müşteri adaylarını (leads) JSON formatında dışarı aktarır.
    """
    adaylar = tum_adaylari_getir()
    return jsonify({"basari": True, "toplam": len(adaylar), "adaylar": adaylar})

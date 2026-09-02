from flask import Blueprint, request, jsonify, render_template
from app.services.ai_service import AIService, YapayZekaServisHatasi
from app.database import musteri_adayi_ekle, tum_adaylari_getir
from flask_cors import cross_origin

# Rotaları gruplandırmak için Blueprint (Taslak) nesneleri oluşturuyoruz.
api_interface = Blueprint("api", __name__)

# ─── API UÇ NOKTALARI (Endpoints) ──────────────────────
@api_interface.route("/sohbet", methods=["POST"])
@cross_origin()  
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
        yanit = AIService.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "cevap": yanit})
    except YapayZekaServisHatasi as e:
        return jsonify({"basari": False, "hata": str(e)}), 503

@api_interface.route("/adaylar", methods=["POST"])
@cross_origin()  
def aday_kaydet():
    """
    Ziyaretçinin iletişim formundan gönderdiği isim ve telefon bilgilerini
    alır ve veritabanı katmanını kullanarak kaydeder.
    """
    veri = request.json
    isim = veri.get("isim")
    mail = veri.get("mail")
    mesaj = veri.get("mesaj")

    #if not isim or not mail:
    #    return jsonify({"basari": False, "hata": "İsim ve mail bilgisi zorunludur."}), 400

    musteri_adayi_ekle(isim, mail, mesaj)
    return jsonify({"basari": True, "mesaj": "Bilgileriniz başarıyla sistemimize kaydedildi."})

@api_interface.route("/adaylar", methods=["GET"])
@cross_origin()  
def adaylari_listele():
    """
    Yönetim panelindeki tabloyu doldurmak için veritabanındaki 
    tüm müşteri adaylarını (leads) JSON formatında dışarı aktarır.
    """
    adaylar = tum_adaylari_getir()
    return jsonify({"basari": True, "toplam": len(adaylar), "adaylar": adaylar})

import sqlite3
from flask import current_app

def baglanti_al():
    # İNGİLİZCE STANDARTLARA GÖRE GÜNCELLENDİ (DATABASE_URL)
    vt_yolu = current_app.config.get("DATABASE_URL", "akilli_satis.db")
    baglanti = sqlite3.connect(vt_yolu)
    baglanti.row_factory = sqlite3.Row
    return baglanti

def initialize_database(uygulama):
    with uygulama.app_context():
        baglanti = baglanti_al()
        imlec = baglanti.cursor()
        imlec.execute('''
            CREATE TABLE IF NOT EXISTS musteri_adaylari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                mail TEXT NOT NULL,
                mesaj TEXT,
                olusturulma_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        baglanti.commit()
        baglanti.close()

def musteri_adayi_ekle(isim: str, mail: str, mesaj: str):
    baglanti = baglanti_al()
    imlec = baglanti.cursor()
    imlec.execute(
        "INSERT INTO musteri_adaylari (isim, mail, mesaj) VALUES (?, ?, ?)",
        (isim, mail, mesaj)
    )
    baglanti.commit()
    baglanti.close()

def tum_adaylari_getir() -> list:
    baglanti = baglanti_al()
    imlec = baglanti.cursor()
    imlec.execute("SELECT * FROM musteri_adaylari ORDER BY olusturulma_tarihi DESC")
    satirlar = imlec.fetchall()
    baglanti.close()
    
    adaylar = []
    for satir in satirlar:
        adaylar.append({
            "id": satir["id"],
            "isim": satir["isim"],
            "mail": satir["mail"],
            "mesaj": satir["mesaj"],
            "olusturulma_tarihi": satir["olusturulma_tarihi"]
        })
    return adaylar

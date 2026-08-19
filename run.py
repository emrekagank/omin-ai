# OMIN KURUMSAL BİLİŞİM TEKNOLOJİLERİ LİMİTED ŞİRKETİ AI SOHBET BOTU PROJESİNİN BAŞLANGIÇ DOSYASIDIR

from app import initialize_app

omin = initialize_app()

if __name__ == "__main__":
   
    omin.run(host="0.0.0.0", port=5000, debug=True)
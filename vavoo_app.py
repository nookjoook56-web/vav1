import requests

def create_m3u():
    # 404 hatasını önlemek için alternatif linkleri deneyelim
    # Önce 'master' dalını deniyoruz, çünkü bazen 'main' yerine 'master' kullanılır.
    source_url = "https://raw.githubusercontent.com/nookjoook56-web/Update-m3u/master/playlist.m3u"
    
    try:
        print(f"🛰️ Liste indiriliyor: {source_url}")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(source_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            with open("vavoo_app.m3u8", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("✅ vavoo_app.m3u8 başarıyla oluşturuldu!")
        else:
            print(f"❌ Hata: Dosya bulunamadı! Durum kodu: {response.status_code}")
            # Eğer hala 404 alıyorsa diğer ihtimali deneyelim
            print("💡 İpucu: playlist.m3u dosyasının doğru linkini kopyalayıp buraya yapıştırın.")
            
    except Exception as e:
        print(f"❌ Bir hata oluştu: {e}")

if __name__ == "__main__":
    create_m3u()
    

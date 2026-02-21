import requests

def create_m3u():
    # Burası senin asıl kanal listesinin (m3u) linki
    source_url = "https://raw.githubusercontent.com/nookjoook56-web/Update-m3u/main/playlist.m3u"
    
    try:
        print("🛰️ Liste indiriliyor...")
        response = requests.get(source_url)
        if response.status_code == 200:
            # İndirilen içeriği yeni bir dosyaya kaydediyoruz
            with open("vavoo_app.m3u8", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("✅ vavoo_app.m3u8 başarıyla oluşturuldu!")
        else:
            print(f"❌ Hata: Kaynak dosya alınamadı. Kod: {response.status_code}")
    except Exception as e:
        print(f"❌ Bir hata oluştu: {e}")

if __name__ == "__main__":
    create_m3u()
  

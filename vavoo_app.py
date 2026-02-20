import requests
import os
import re

# Vavoo'nun güncel config adresi
VAVOO_CONFIG = "https://vavoo.to/config"

def get_vavoo_token():
    headers = {
        'User-Agent': 'VAVOO/2.6',
        'Accept': 'application/json'
    }
    print("🛰️ Token çekiliyor...")
    try:
        # GitHub sunucuları bazen engellendiği için timeout'u uzun tutuyoruz
        response = requests.get(VAVOO_CONFIG, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data.get('signed') or data.get('token')
    except Exception as e:
        print(f"❌ Token alınamadı: {e}")
    return None

def create_m3u8():
    token = get_vavoo_token()
    if not token:
        return

    # Kendi kanal listen (Buraya istediğin kanalları ekle)
    channels = [
        ("https://vavoo.to/live2/play3/593493860.m3u8", "TR: beIN Sports 1"),
        ("https://vavoo.to/live2/play3/165415732.m3u8", "TR: beIN Sports 2"),
        ("https://vavoo.to/live2/play3/845123654.m3u8", "TR: beIN Sports 3"),
        ("https://vavoo.to/live2/kanald.m3u8", "TR: Kanal D"),
        ("https://vavoo.to/live2/atv.m3u8", "TR: ATV")
    ]

    print("📄 Dosya oluşturuluyor...")
    with open("vavoo_app.m3u8", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for url, name in channels:
            # Token'ı linklerin sonuna ekliyoruz
            f.write(f"#EXTINF:-1,{name}\n{url}?token={token}\n")
    
    print("✅ Liste başarıyla hazırlandı.")

if __name__ == "__main__":
    create_m3u8()
  

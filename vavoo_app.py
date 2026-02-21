import requests
import json
import os

def get_vavoo_channels():
    # Vavoo'nun JSON formatındaki kanal listesi
    url = "https://www2.vavoo.to/live2/index?output=json"
    headers = {
        'User-Agent': 'VAVOO/2.6',
        'Content-Type': 'application/json; charset=utf-8'
    }

    try:
        print("🛰️ Vavoo kanalları çekiliyor...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            channels = response.json()
            
            # M3U Dosyasını Oluşturma
            with open("vavoo_app.m3u8", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                
                for c in channels:
                    # Sadece belirli ülkeleri veya hepsini filtreleyebilirsin
                    # Örn: if c['group'] == 'Turkey':
                    name = c.get('name', 'Unknown')
                    logo = c.get('logo', '')
                    group = c.get('group', 'Vavoo')
                    url = c.get('url', '')
                    
                    f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
                    f.write(f'#EXTVLCOPT:http-user-agent=VAVOO/2.6\n')
                    f.write(f'{url}\n')
            
            print(f"✅ Başarılı! {len(channels)} kanal listeye eklendi.")
        else:
            print(f"❌ Hata: Vavoo API cevap vermedi. Kod: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Bir hata oluştu: {e}")

if __name__ == "__main__":
    get_vavoo_channels()
    

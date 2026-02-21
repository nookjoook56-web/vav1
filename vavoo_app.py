import requests
import json

def get_vavoo_with_headers():
    # Vavoo API adresi
    url = "https://www2.vavoo.to/live2/index?output=json"
    
    # Sunucunun bizi reddetmemesi için gerekli olan tarayıcı/uygulama bilgisi
    headers = {
        'User-Agent': 'VAVOO/2.6',
        'Content-Type': 'application/json; charset=utf-8'
    }

    try:
        print("🛰️ Vavoo verileri ve Header bilgileri alınıyor...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            channels = response.json()
            
            with open("vavoo_app.m3u8", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                
                for c in channels:
                    name = c.get('name', 'Unknown')
                    logo = c.get('logo', '')
                    group = c.get('group', 'Vavoo')
                    stream_url = c.get('url', '')
                    
                    # Kanal bilgisi
                    f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
                    
                    # --- KRİTİK HEADER KISMI ---
                    # Bu satır, oynatıcıya "bu linki açarken Vavoo gibi davran" der.
                    f.write(f'#EXTVLCOPT:http-user-agent=VAVOO/2.6\n')
                    f.write(f'#EXTHTTP:{{"User-Agent":"VAVOO/2.6"}}\n')
                    
                    # Linkin sonuna da bazı oynatıcılar için header ekleyebiliriz
                    f.write(f'{stream_url}|User-Agent=VAVOO/2.6\n')
            
            print(f"✅ İşlem tamam! {len(channels)} kanal Header bilgileriyle kaydedildi.")
        else:
            print(f"❌ API Hatası: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Script çalışırken hata oluştu: {e}")

if __name__ == "__main__":
    get_vavoo_with_headers()
    

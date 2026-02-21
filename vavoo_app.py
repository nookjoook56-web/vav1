import requests
import json
import random

def get_vavoo_signature():
    try:
        # Vavoo'nun imza (signed) anahtarını aldığı ping servisi
        # Bu liste michaz gibi geliştiricilerin güncel tuttuğu anahtar listesidir
        veclist = requests.get("https://raw.githubusercontent.com/michaz1988/michaz1988.github.io/master/data.json").json()
        vec = {"vec": random.choice(veclist)}
        req = requests.post('https://www.vavoo.tv/api/box/ping2', data=vec).json()
        
        # Farklı API versiyonlarına göre imzayı yakala
        sig = req.get('signed') or req.get('data', {}).get('signed') or req.get('response', {}).get('signed')
        return sig
    except:
        return None

def main():
    sig = get_vavoo_signature()
    if not sig:
        print("❌ İmza alınamadı, standart modda devam ediliyor...")
        sig = ""
    else:
        print(f"✅ İmza başarıyla alındı: {sig[:10]}...")

    url = "https://www2.vavoo.to/live2/index?output=json"
    headers = {'User-Agent': 'VAVOO/2.6'}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            channels = response.json()
            with open("vavoo_app.m3u8", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                for c in channels:
                    name = c.get('name', 'Unknown')
                    group = c.get('group', 'Vavoo')
                    logo = c.get('logo', '')
                    # Linkin sonuna imzayı (signature) ekliyoruz
                    stream_url = f"{c.get('url')}?n=1&sig={sig}"
                    
                    f.write(f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n')
                    f.write(f'#EXTVLCOPT:http-user-agent=VAVOO/2.6\n')
                    f.write(f'{stream_url}\n')
            print("✅ Liste ve imzalar güncellendi.")
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    main()
        

import requests
import json
import random

def get_vavoo_signature():
    try:
        veclist = requests.get("https://raw.githubusercontent.com/michaz1988/michaz1988.github.io/master/data.json").json()
        vec = {"vec": random.choice(veclist)}
        req = requests.post('https://www.vavoo.tv/api/box/ping2', data=vec).json()
        sig = req.get('signed') or req.get('data', {}).get('signed') or req.get('response', {}).get('signed')
        return sig
    except:
        return None

def main():
    sig = get_vavoo_signature()
    if not sig:
        sig = ""

    url = "https://www2.vavoo.to/live2/index?output=json"
    headers = {'User-Agent': 'VAVOO/2.6'}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            channels = response.json()
            
            # Kanalları ayırmak için iki liste oluşturuyoruz
            sports_list = []
            other_list = []

            for c in channels:
                name = c.get('name', '').upper()
                group = c.get('group', 'Vavoo')
                logo = c.get('logo', '')
                stream_url = f"{c.get('url')}?n=1&sig={sig}"
                
                # Bein Sport, Sports, Digi kelimelerini içeren kanalları ayır
                if any(x in name for x in ["BEIN", "SPORT", "DIGI"]) and group == "Turkey":
                    entry = f'#EXTINF:-1 tvg-logo="{logo}" group-title="Bein Sports",{name}\n#EXTVLCOPT:http-user-agent=VAVOO/2.6\n{stream_url}\n'
                    sports_list.append(entry)
                else:
                    entry = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n#EXTVLCOPT:http-user-agent=VAVOO/2.6\n{stream_url}\n'
                    other_list.append(entry)

            # Dosyaya önce spor kanallarını, sonra diğerlerini yazıyoruz
            with open("vavoo_app.m3u8", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                # Önce ayırdığımız spor listesi
                for item in sports_list:
                    f.write(item)
                # Sonra geri kalan her şey
                for item in other_list:
                    f.write(item)
                    
            print(f"✅ Ayrıştırma tamam! {len(sports_list)} spor kanalı başa eklendi.")
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    main()
    

import requests
import json
import random

def get_vavoo_signature():
    try:
        # Güncel signature anahtarları için michaz listesini kullanıyoruz
        veclist = requests.get("https://raw.githubusercontent.com/michaz1988/michaz1988.github.io/master/data.json").json()
        vec = {"vec": random.choice(veclist)}
        req = requests.post('https://www.vavoo.tv/api/box/ping2', data=vec).json()
        return req.get('signed') or req.get('data', {}).get('signed') or req.get('response', {}).get('signed')
    except:
        return None

def main():
    sig = get_vavoo_signature()
    headers = {'User-Agent': 'VAVOO/2.6'}
    url = "https://www2.vavoo.to/live2/index?output=json"

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            channels = response.json()
            bein_list = []
            other_list = []

            for c in channels:
                name = c.get('name', '').upper()
                group = c.get('group', 'Vavoo')
                logo = c.get('logo', '')
                # Bağlantı hatasını önlemek için linke imzayı ekliyoruz
                stream_url = f"{c.get('url')}?n=1&sig={sig}" if sig else c.get('url')
                
                # Header bilgilerini player'ın anlaması için formatlıyoruz
                # Bu kısım SSL ve Connection Reset hatalarını önlemek içindir
                header_info = '#EXTVLCOPT:http-user-agent=VAVOO/2.6\n#EXTHTTP:{"User-Agent":"VAVOO/2.6"}'
                
                # Bein Sport Filtreleme (Sadece Türkiye grubundaki Bein'ler)
                if "BEIN" in name and group == "Turkey":
                    entry = f'#EXTINF:-1 tvg-logo="{logo}" group-title="BEIN SPORTS",{name}\n{header_info}\n{stream_url}|User-Agent=VAVOO/2.6\n'
                    bein_list.append(entry)
                else:
                    entry = f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n{header_info}\n{stream_url}|User-Agent=VAVOO/2.6\n'
                    other_list.append(entry)

            with open("vavoo_app.m3u8", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                # Önce Bein Sport kanalları
                for item in bein_list:
                    f.write(item)
                # Sonra diğer tüm kanallar
                for item in other_list:
                    f.write(item)
            
            print(f"✅ İşlem Başarılı! {len(bein_list)} Bein kanalı ayrıldı ve en başa eklendi.")
    except Exception as e:
        print(f"❌ Hata oluştu: {e}")

if __name__ == "__main__":
    main()

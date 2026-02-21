import requests
import json
import random

def get_vavoo_signature():
    try:
        # Vavoo Signature (İmza) almak için güncel anahtar havuzu
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
        print("⚠️ İmza alınamadı, linkler çalışmayabilir.")
    
    url = "https://www2.vavoo.to/live2/index?output=json"
    headers = {'User-Agent': 'VAVOO/2.6'}

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
                base_url = c.get('url', '')
                
                # RESOLVER MANTIĞI: Linke imza ve gerekli header'ları gömüyoruz
                # Bu format OTT Navigator ve VLC gibi oynatıcılarda 'çözücü' görevi görür
                resolved_url = f"{base_url}?n=1&sig={sig}" if sig else base_url
                
                # Header tanımlamaları (SSL ve Connection Reset hatalarını aşmak için)
                m3u_entry = (
                    f'#EXTINF:-1 tvg-logo="{logo}" group-title="{"BEIN SPORTS" if "BEIN" in name and group == "Turkey" else group}",{name}\n'
                    f'#EXTVLCOPT:http-user-agent=VAVOO/2.6\n'
                    f'#EXTHTTP:{{"User-Agent":"VAVOO/2.6"}}\n'
                    f'{resolved_url}|User-Agent=VAVOO/2.6\n'
                )

                if "BEIN" in name and group == "Turkey":
                    bein_list.append(m3u_entry)
                else:
                    other_list.append(m3u_entry)

            with open("vavoo_app.m3u8", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                # Önce çözülmüş Bein kanalları
                f.writelines(bein_list)
                # Sonra diğerleri
                f.writelines(other_list)
            
            print(f"✅ Resolver aktif: {len(bein_list)} Bein kanalı hazır!")
    except Exception as e:
        print(f"❌ Kritik Hata: {e}")

if __name__ == "__main__":
    main()
    

import sys
import requests
import json
import re

# Yapılandırma - Doğrudan vavoo.to odaklı
BASE_URL = "https://vavoo.to"
API_URL = "https://www.vavoo.tv/api/app/ping" # İmza (Signature) hala ana API üzerinden alınır

def get_auth_signature():
    """Vavoo sunucularından güncel erişim imzasını alır."""
    headers = {
        "user-agent": "okhttp/4.11.0",
        "accept": "application/json",
        "content-type": "application/json; charset=utf-8"
    }
    
    # Bu veri paketi cihazı taklit eder. Token geçersizleşirse yenilenmelidir.
    payload = {
        "token": "tosFwQCJMS8qrW_AjLoHPQ41646J5dRNha6ZWHnijoYQQQoADQoXYSo7ki7O5-CsgN4CH0uRk6EEoJ0728ar9scCRQW3ZkbfrPfeCXW2VgopSW2FWDqPOoVYIuVPAOnXCZ5g",
        "reason": "app focus",
        "locale": "de",
        "metadata": {
            "device": {"brand": "google", "model": "Nexus"},
            "os": {"name": "android", "version": "7.1.2"},
            "app": {"platform": "android", "version": "3.1.20"}
        },
        "package": "tv.vavoo.app",
        "version": "3.1.20"
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        sig = response.json().get("addonSig")
        if sig:
            return sig
    except Exception as e:
        print(f"⚠️ İmza alınamadı: {e}", file=sys.stderr)
    return None

def fetch_vavoo_channels(group_name="Turkey"):
    """vavoo.to üzerinden kanal listesini çeker."""
    sig = get_auth_signature()
    if not sig:
        return []

    headers = {
        "user-agent": "okhttp/4.11.0",
        "mediahubmx-signature": sig
    }

    all_channels = []
    cursor = 0
    
    print(f"📡 {group_name} grubu için vavoo.to üzerinden veriler çekiliyor...")

    while True:
        payload = {
            "language": "tr",
            "region": "TR",
            "catalogId": "iptv",
            "id": "iptv",
            "filter": {"group": group_name},
            "cursor": cursor
        }
        
        try:
            # Doğrudan vavoo.to kataloğuna istek atıyoruz
            resp = requests.post(f"{BASE_URL}/mediahubmx-catalog.json", json=payload, headers=headers, timeout=10)
            data = resp.json()
            
            items = data.get("items", [])
            all_channels.extend(items)
            
            cursor = data.get("nextCursor")
            if not cursor:
                break
        except Exception as e:
            print(f"❌ Veri çekme hatası: {e}")
            break
            
    return all_channels

def create_m3u():
    # Sadece Türkiye kanallarını veya istediğin diğer ülkeleri ekleyebilirsin
    target_groups = ["Turkey", "Germany"] 
    
    with open("vavoo_v2.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for group in target_groups:
            channels = fetch_vavoo_channels(group)
            for ch in channels:
                name = ch.get("name", "Unknown")
                # URL'i vavoo-iptv formatına dönüştürerek oynatılabilir yapıyoruz
                raw_url = ch.get("url", "")
                final_url = raw_url.replace("/play/", "/vavoo-iptv/play/")
                
                f.write(f'#EXTINF:-1 group-title="{group}",{name}\n')
                f.write(f"{final_url}\n")
    
    print(f"✨ Liste hazır: vavoo_v2.m3u")

if __name__ == "__main__":
    create_m3u()
    

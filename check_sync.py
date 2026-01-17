import requests
import json

PROWLARR_URL = "http://localhost:9696"
PROWLARR_API_KEY = "88c41e7efe9b4f71b7793711c79ec562"
HEADERS = {
    "X-Api-Key": PROWLARR_API_KEY,
    "Content-Type": "application/json"
}

def check_sync():
    print("Checking Prowlarr Status...")
    
    # 1. Check Indexers
    try:
        resp = requests.get(f"{PROWLARR_URL}/api/v1/indexer", headers=HEADERS)
        resp.raise_for_status()
        indexers = resp.json()
        geek_indexer = next((i for i in indexers if 'nzbgeek' in i['name'].lower()), None)
        
        if geek_indexer:
            print(f"[OK] Found Indexer: {geek_indexer['name']}")
        else:
            print("[FAIL] NZBGeek indexer NOT found in Prowlarr.")
    except Exception as e:
        print(f"[Error] Failed to fetch indexers: {e}")
        return

    # 2. Check Applications (Sonarr/Radarr)
    try:
        resp = requests.get(f"{PROWLARR_URL}/api/v1/applications", headers=HEADERS)
        resp.raise_for_status()
        print(f"RAW RESP: {resp.text}")
        apps = resp.json()
        
        print(f"Found {len(apps)} Applications:")
        for app in apps:
            name = app.get('name', 'Unknown')
            sync_level = app.get('syncLevel', 'Unknown')
            # Check if indexer is disabled for this app? Can't easily see per-indexer per-app without more digging, 
            # but usually it's global or profile based.
            # However, we can see if the app itself is set to sync 'full' or 'addOnly' etc.
            print(f" - {name}: SyncLevel={sync_level}")
            
    except Exception as e:
        print(f"[Error] Failed to fetch applications: {e}")

if __name__ == "__main__":
    check_sync()

import requests
import json

PROWLARR_URL = "https://prowlarr.138.199.156.62.sslip.io"
PROWLARR_API_KEY = "88c41e7efe9b4f71b7793711c79ec562"
HEADERS = {
    "X-Api-Key": PROWLARR_API_KEY,
    "Content-Type": "application/json"
}

TARGETS = ["Lat-Team", "PuntoTorrent"]

def get_requirements():
    print("Fetching schemas...")
    try:
        resp = requests.get(f"{PROWLARR_URL}/api/v1/indexer/schema", headers=HEADERS)
        resp.raise_for_status()
        schemas = resp.json()
    except Exception as e:
        print(f"Error: {e}")
        return

    schema_map = {s['name'].lower(): s for s in schemas}

    print("\n--- Credential Requirements ---\n")
    for target in TARGETS:
        # fuzzy match
        found = None
        for name, s in schema_map.items():
            if target.lower() in name:
                found = s
                break
        
        if found:
            print(json.dumps(found, indent=2))
        else:
            print(f"Could not find schema for {target}")

if __name__ == "__main__":
    get_requirements()

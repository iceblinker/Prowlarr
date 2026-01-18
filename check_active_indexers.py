import requests

PROWLARR_URL = "https://prowlarr.138.199.156.62.sslip.io"
API_KEY = "b8964a3d3477cade9ad4ce916a30d5b5"

def check_indexers():
    try:
        resp = requests.get(f"{PROWLARR_URL}/api/v1/indexer", headers={"X-Api-Key": API_KEY})
        resp.raise_for_status()
        indexers = resp.json()
        
        print(f"Found {len(indexers)} indexers:")
        for i in indexers:
            print(f"- {i['name']} (Tags: {i['tags']})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_indexers()

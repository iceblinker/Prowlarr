import os
import requests
import json

# Manual .env parser to avoid installing python-dotenv on VPS
def load_env_manual():
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

load_env_manual()

PROWLARR_URL = "http://localhost:9696"
# Try to get from Env, fallback to verified hardcoded (repo) keys
PROWLARR_API_KEY = os.getenv("PROWLARR_API_KEY", "88c41e7efe9b4f71b7793711c79ec562")
HEADERS = {
    "X-Api-Key": PROWLARR_API_KEY,
    "Content-Type": "application/json"
}

# Shared Keys from .env
SONARR_API_KEY = os.getenv("SONARR_API_KEY", "526ef90ca47d38b1")
RADARR_API_KEY = os.getenv("RADARR_API_KEY", "de79f80c6b35a214")
PROWLARR_INTERNAL_URL = "http://gluetun:9696"

APPS = [
    {
        "name": "Sonarr EN",
        "appName": "Sonarr",
        "baseUrl": "http://sonarr-en:8989",
        "apiKey": SONARR_API_KEY,
        "implementation": "Sonarr"
    },
    {
        "name": "Sonarr ES",
        "appName": "Sonarr",
        "baseUrl": "http://sonarr-es:8989",
        "apiKey": SONARR_API_KEY,
        "implementation": "Sonarr"
    },
    {
        "name": "Sonarr IT",
        "appName": "Sonarr",
        "baseUrl": "http://sonarr-it:8989",
        "apiKey": SONARR_API_KEY,
        "implementation": "Sonarr"
    },
    {
        "name": "Radarr EN",
        "appName": "Radarr",
        "baseUrl": "http://radarr-en:7878",
        "apiKey": RADARR_API_KEY,
        "implementation": "Radarr"
    },
    {
        "name": "Radarr ES",
        "appName": "Radarr",
        "baseUrl": "http://radarr-es:7878",
        "apiKey": RADARR_API_KEY,
        "implementation": "Radarr"
    },
    {
        "name": "Radarr IT",
        "appName": "Radarr",
        "baseUrl": "http://radarr-it:7878",
        "apiKey": RADARR_API_KEY,
        "implementation": "Radarr"
    }
]

def configure_apps():
    print("Configuring Prowlarr Applications...")
    
    for app in APPS:
        payload = {
            "name": app["name"],
            "syncLevel": "fullSync",
            "fields": [
                { "name": "prowlarrUrl", "value": PROWLARR_INTERNAL_URL },
                { "name": "baseUrl", "value": app["baseUrl"] },
                { "name": "apiKey", "value": app["apiKey"] }
            ],
            "implementationName": app["implementation"],
            "implementation": app["implementation"],
            "configContract": f"{app['implementation']}Settings",
            "tags": []
        }
        
        try:
            print(f"Adding {app['name']}...")
            resp = requests.post(f"{PROWLARR_URL}/api/v1/applications", headers=HEADERS, json=payload)
            if resp.status_code == 201:
                print(f" -> Success")
            else:
                print(f" -> Failed: {resp.status_code} - {resp.text}")
            if resp.status_code == 400:
                with open("last_error.json", "w") as f:
                    f.write(resp.text)
                print("DEBUG: Error saved to last_error.json")
        except Exception as e:
            print(f" -> Error: {e}")

if __name__ == "__main__":
    configure_apps()

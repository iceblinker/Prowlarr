import requests
import json

PROWLARR_URL = "https://prowlarr.138.199.156.62.sslip.io"
PROWLARR_API_KEY = "88c41e7efe9b4f71b7793711c79ec562"
HEADERS = {
    "X-Api-Key": PROWLARR_API_KEY,
    "Content-Type": "application/json"
}

TARGETS = {
    "Italian": ["ItaTorrents", "ShareIsland", "ArabaFenice", "1337x", "Badass Torrents"],
    "Spanish": ["HD-Spain", "PuntoTorrent", "HD-Olimpo", "DonTorrent", "Elite Torrent"],
    "Latino": ["Lat-Team", "ChileBT", "TorrentLandia", "Identi", "DivxTotal", "DescargasDD"],
    "Usenet": ["NZBGeek", "DrunkenSlug", "nzb.su"]
}

def analyze_targets():
    print("Fetching indexer schemas from Prowlarr...")
    try:
        resp = requests.get(f"{PROWLARR_URL}/api/v1/indexer/schema", headers=HEADERS)
        resp.raise_for_status()
        schemas = resp.json()
    except Exception as e:
        print(f"Error fetching schemas: {e}")
        return

    print(f"Total Schemas Found: {len(schemas)}")
    schema_map = {s['name'].lower(): s for s in schemas}
    
    with open("final_report.txt", "w", encoding="utf-8") as f:
        f.write("\n--- Prowlarr Indexer Availability Report ---\n\n")
        for region, trackers in TARGETS.items():
            f.write(f"### {region}\n")
            for tracker in trackers:
                found = None
                if tracker.lower() in schema_map:
                    found = schema_map[tracker.lower()]
                else:
                    for s_name in schema_map:
                        if tracker.lower() in s_name or s_name in tracker.lower():
                            if len(tracker) > 3: 
                                found = schema_map[s_name]
                                break
                
                if found:
                    privacy = found.get('privacy', 'Unknown')
                    protocol = found.get('protocol', 'Unknown')
                    f.write(f"- [x] **{tracker}**: Found as '{found['name']}' ({protocol}, {privacy})\n")
                else:
                    f.write(f"- [ ] **{tracker}**: NOT FOUND in Prowlarr definitions.\n")
    print("Report written to final_report.txt")

if __name__ == "__main__":
    analyze_targets()

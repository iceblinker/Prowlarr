import argparse
import requests
import json
import os

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
PROWLARR_URL = os.getenv("PROWLARR_URL", "http://localhost:9696")
PROWLARR_API_KEY = os.getenv("PROWLARR_API_KEY", "")

def get_search_params_from_ai(query):
    """Asks Ollama to extract title and language tags."""
    print(f"🤖 Asking AI to understand: '{query}'...")
    
    prompt = (
        f"Analyze this search query: '{query}'. "
        "Extract the media title and identifying language tags/categories if the user asks for specific languages (Spanish, Italian, etc). "
        "Return ONLY a JSON object with keys: 'title' (string), 'tags' (list of strings, e.g. ['ESP', 'Multi']), 'categories' (list of integers, e.g. [5000]). "
        "If no language specified, return empty tags. Do not output markdown."
    )
    
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": "llama3", 
            "prompt": prompt,
            "stream": False,
            "format": "json"
        })
        resp.raise_for_status()
        data = resp.json()
        return json.loads(data['response'])
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return None

def search_prowlarr(params):
    """Searches Prowlarr using parsed parameters."""
    query = params.get('title')
    print(f"🔍 Searching Prowlarr for: '{query}' with tags: {params.get('tags')}...")
    
    if not PROWLARR_API_KEY:
        print("❌ Error: PROWLARR_API_KEY is not set.")
        return

    # Simplified search - in a real app you'd append tags to the query or use specific indexer flags
    # Prowlarr API is basic, so we often just append tags to the search query for text matching
    search_query = query
    if params.get('tags'):
        search_query += " " + " ".join(params['tags'])

    try:
        resp = requests.get(f"{PROWLARR_URL}/api/v1/search", params={
            "query": search_query,
            "apikey": PROWLARR_API_KEY,
            "categories": params.get('categories', [])
        })
        resp.raise_for_status()
        results = resp.json()
        print(f"✅ Found {len(results)} results.")
        for item in results[:5]: # Show top 5
            print(f" - {item.get('title')} ({item.get('indexer')})")
    except Exception as e:
        print(f"❌ Prowlarr Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Ask Prowlarr using Natural Language")
    parser.add_argument("query", type=str, help="The natural language query (e.g. 'Find La Casa de Papel in Italian')")
    args = parser.parse_args()

    params = get_search_params_from_ai(args.query)
    if params and params.get('title'):
        search_prowlarr(params)
    else:
        print("Could not identify title.")

if __name__ == "__main__":
    main()

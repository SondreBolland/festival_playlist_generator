import os
import json
import requests
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
import os

from setlist_api.mbids import artist_mbid

load_dotenv()

SETLISTFM_API_KEY = os.getenv("SETLISTFM_API_KEY")
USER_AGENT = os.getenv("USER_AGENT")

CACHE_DIR = Path("setlist_api" ,"setlist_cache")
BASE_URL = "https://api.setlist.fm/rest/1.0"

HEADERS = {
    "x-api-key": SETLISTFM_API_KEY,
    "Accept": "application/json",
    "User-Agent": USER_AGENT,
}

API_CALL_DELAY = 3 # seconds

def ensure_cache_dir():
    """Create the cache directory if it doesn't exist."""
    os.makedirs(CACHE_DIR, exist_ok=True)

def load_cached_setlists(mbid):
    """Load cached setlists for an artist using their MBID."""
    path = os.path.join(CACHE_DIR, f"{mbid}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_cached_setlists(artist, data):
    """Save setlist data to a local JSON file for caching."""
    path = os.path.join(CACHE_DIR, f"{artist}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def fetch_setlists_from_api(mbid, limit=3):
    """Fetch recent setlists from the Setlist.fm API for a given artist MBID."""
    url = f"{BASE_URL}/artist/{mbid}/setlists"
    params = {"p": 1}
    extracted_setlists = []

    while len(extracted_setlists) < limit:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}, {response.text}")
        
        sleep(API_CALL_DELAY)  # Respect API rate limit
        
        page_data = response.json()
        page_setlists = page_data.get("setlist", [])

        # Filter out setlists without songs
        valid_setlists = [
            sl for sl in page_setlists
            if sl.get("sets") and any(
                s.get("song") for s in (sl["sets"].get("set") or [])
            )
        ]

        for sl in valid_setlists:
            # Extract only the songs per setlist
            songs = []
            sets = sl["sets"].get("set") or []
            for set_part in sets:
                for song in set_part.get("song", []):
                    song_name = song.get("name")
                    songs.append(song_name)

            # Store relevant setlist info including URL
            extracted_setlists.append({
                "id": sl.get("id"),
                "eventDate": sl.get("eventDate"),
                "url": sl.get("url"),
                "songs": songs
            })

            if len(extracted_setlists) >= limit:
                break

        if len(page_setlists) == 0 or len(extracted_setlists) >= limit:
            break
        params["p"] += 1

    return extracted_setlists[:limit]

def get_setlists(artist, limit=3):
    """Get recent setlists for an artist, using cache if it has enough entries."""
    print(f"Fetching setlists for {artist}.")
    
    mbid = artist_mbid[artist]
    
    ensure_cache_dir()
    cached = load_cached_setlists(artist)
    
    if cached and len(cached) >= limit:
        return cached[:limit]

    fresh = fetch_setlists_from_api(mbid, limit=limit)
    save_cached_setlists(artist, fresh)
    return fresh


if __name__ == "__main__":
    example_artist = 'Muse'
    get_setlists(example_artist)
    # Now check if the artist's setlists are stored in setlist_api/setlist_cache/<artist>

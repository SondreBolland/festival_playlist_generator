import os
import json
import requests
from time import sleep
from dotenv import load_dotenv
import os

from setlist_api.mbids import artist_mbid

load_dotenv()

SETLISTFM_API_KEY = os.getenv("SETLISTFM_API_KEY")
USER_AGENT = os.getenv("USER_AGENT")

CACHE_DIR = "setlist_cache"
BASE_URL = "https://api.setlist.fm/rest/1.0"

HEADERS = {
    "x-api-key": SETLISTFM_API_KEY,
    "Accept": "application/json",
    "User-Agent": USER_AGENT,
}

def ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)

def load_cached_setlists(mbid):
    path = os.path.join(CACHE_DIR, f"{mbid}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_cached_setlists(artist, data):
    path = os.path.join(CACHE_DIR, f"{artist}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def fetch_setlists_from_api(mbid, limit=3):
    url = f"{BASE_URL}/artist/{mbid}/setlists"
    params = {"p": 1}
    extracted_setlists = []

    while len(extracted_setlists) < limit:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code}, {response.text}")
        
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

        sleep(2)  # Respect API rate limit

    return extracted_setlists[:limit]


def get_setlists(artist, limit=3):
    # Fetch the artist's mbid
    mbid = artist_mbid[artist]
    
    ensure_cache_dir()
    cached = load_cached_setlists(artist)
    if cached:
        return cached

    fresh = fetch_setlists_from_api(mbid, limit=limit)
    save_cached_setlists(artist, fresh)
    return fresh

if __name__ == "__main__":
    for artist in artist_mbid.keys():
        setlists = get_setlists(artist)
        print(f"Fetched setlists for {artist}")

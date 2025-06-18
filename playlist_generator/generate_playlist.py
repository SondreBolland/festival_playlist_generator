import json
from collections import Counter
from pathlib import Path

def load_setlists(file_path):
    """Load setlist data from JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_most_common_songs(setlists, limit=20):
    """Return the most common songs across all setlists, limited to a given number."""
    all_songs = []
    for setlist in setlists:
        all_songs.extend(setlist["songs"])
    counter = Counter(all_songs)
    most_common = [song for song, _ in counter.most_common(limit)]
    return most_common

def get_all_unique_songs(setlists):
    """Return a list of all unique songs from all setlists."""
    all_songs = set()
    for setlist in setlists:
        all_songs.update(setlist["songs"])
    return sorted(all_songs)

def generate_playlists(file_path, top_n=20):
    """Generates both types of playlists from the input file."""
    setlists = load_setlists(file_path)
    most_common_playlist = get_most_common_songs(setlists, limit=top_n)
    unique_playlist = get_all_unique_songs(setlists)
    return most_common_playlist, unique_playlist

if __name__ == "__main__":
    # Example usage with Muse.json
    artist_file = Path("setlist_cache/Muse.json")  # Adjust path if needed
    top_n = 15  # You can change this as a setting

    most_common, unique = generate_playlists(artist_file, top_n=top_n)

    print("Most common songs playlist:")
    for song in most_common:
        print("-", song)

    print("\nAll unique songs:")
    for song in unique:
        print("-", song)

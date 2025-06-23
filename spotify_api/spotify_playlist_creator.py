import json
from pathlib import Path
from spotify_api.spotify_auth import get_spotify_client

def search_track_id(sp, track_name, artist):
    if track_name is None:
        raise ValueError("Track was None. Query must have a track.")
    if artist is None:
        raise ValueError("Artist was None. Query must have an artist.")

    # Use Spotify's advanced query syntax for precision
    query = f'track:"{track_name}" artist:"{artist}"'
    results = sp.search(q=query, type='track', limit=5)
    tracks = results.get('tracks', {}).get('items', [])

    # Filter for exact matches on both track title and artist
    track_name_lower = track_name.lower()
    artist_lower = artist.lower()

    for track in tracks:
        title_match = track['name'].lower() == track_name_lower
        artist_match = any(artist_lower == a['name'].lower() for a in track['artists'])

        if artist_match:
            return track['id']

    # Strict: return None if no exact match found
    return None

def create_playlist(sp, user_id, name, description=""):
    playlist = sp.user_playlist_create(user=user_id, name=name, public=True, description=description)
    return playlist['id']

def add_tracks_to_playlist(sp, playlist_id, track_ids):
    CHUNK = 100  # Spotify limit per add call
    for i in range(0, len(track_ids), CHUNK):
        sp.playlist_add_items(playlist_id, track_ids[i:i+CHUNK])

def create_spotify_playlist_from_songs(playlist_name, song_titles, artists):
    sp = get_spotify_client()
    user_id = sp.me()['id']

    track_ids = []
    for song in song_titles:
        track_id = None
        for artist in artists:
            track_id = search_track_id(sp, song, artist)
            if track_id:
                break  # Stop as soon as a match is found
        if track_id:
            track_ids.append(track_id)
        else:
            print(f"Could not find: {song}")

    playlist_id = create_playlist(sp, user_id, playlist_name)
    add_tracks_to_playlist(sp, playlist_id, track_ids)

    print(f"Playlist '{playlist_name}' created with {len(track_ids)} tracks!")



if __name__ == "__main__":
    # Example
    sp = get_spotify_client()
    search_track_id(sp, 'Psycho', 'Muse')
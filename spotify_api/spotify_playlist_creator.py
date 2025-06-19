import json
from pathlib import Path
from spotify_api.spotify_auth import get_spotify_client

def search_track_id(sp, track_name, artist=None):
    query = f"{track_name} {artist}" if artist else track_name
    results = sp.search(q=query, type='track', limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    return tracks[0]['id'] if tracks else None

def create_playlist(sp, user_id, name, description=""):
    playlist = sp.user_playlist_create(user=user_id, name=name, public=True, description=description)
    return playlist['id']

def add_tracks_to_playlist(sp, playlist_id, track_ids):
    CHUNK = 100  # Spotify limit per add call
    for i in range(0, len(track_ids), CHUNK):
        sp.playlist_add_items(playlist_id, track_ids[i:i+CHUNK])

def create_spotify_playlist_from_songs(playlist_name, song_titles, artist):
    sp = get_spotify_client()
    user_id = sp.me()['id']

    track_ids = []
    for song in song_titles:
        track_id = search_track_id(sp, song, artist)
        if track_id:
            track_ids.append(track_id)
        else:
            print(f"Could not find: {song}")

    playlist_id = create_playlist(sp, user_id, playlist_name)
    add_tracks_to_playlist(sp, playlist_id, track_ids)

    print(f"Playlist '{playlist_name}' created with {len(track_ids)} tracks!")

from pathlib import Path
from playlist_generator.generate_playlist import generate_playlists
from spotify_api.spotify_playlist_creator import create_spotify_playlist_from_songs
from setlist_api.mbids import artist_mbid
from setlist_api.get_setlists import get_setlists


# === Configuration variables ===
# List of artist names (must match JSON filenames)
artists = ["Muse", "Avenged Sevenfold", "Green Day", "Megadeth", "Dream Theater", "Dimmu Borgir", "Kaizers Orchestra"]        
# Number of songs per artist if not using unique songs  
songs_per_artist = 15
# Number of concerts to fetch playlists from
n_setlists_per_artist = 3
# True: use all unique songs, False: use the most frequently played songs up to n=songs_per_artist                                    
use_unique_songs = False
# Name of the Spotify playlist
playlist_name = "Tons of Rock 2025"
# True: one playlist with all artists combined, False: one per artist
one_big_playlist = True

def main():
    # Get all artists' setlists
    for artist in artists:
        if artist not in artist_mbid.keys():
            print(f"The mbid for {artist} is missing. Go to https://musicbrainz.org to find it in the {artist}'s page url.")
        get_setlists(artist, n_setlists_per_artist)
    
    all_songs = []

    for artist in artists:
        json_file = Path(f"setlist_api/setlist_cache/{artist}.json")
        if not json_file.exists():
            print(f"Setlist file not found for artist: {artist}")
            continue

        most_common, unique = generate_playlists(json_file, top_n=songs_per_artist)
        selected_songs = unique if use_unique_songs else most_common

        if not selected_songs:
            print(f"No songs found for {artist}")
            continue

        if one_big_playlist:
            all_songs.extend(selected_songs)
        else:
            print(f"Creating playlist for {artist}: '{playlist_name}' with {len(selected_songs)} songs")
            create_spotify_playlist_from_songs(
                playlist_name=f"{playlist_name} - {artist}",
                song_titles=selected_songs,
                artist=artist
            )

    if one_big_playlist and all_songs:
        # Remove duplicates while preserving order
        seen = set()
        combined_songs = [x for x in all_songs if not (x in seen or seen.add(x))]

        print(f"Creating combined playlist: '{playlist_name}' with {len(combined_songs)} songs")
        create_spotify_playlist_from_songs(
            playlist_name=playlist_name,
            song_titles=combined_songs,
            artist=None
        )

if __name__ == "__main__":
    main()


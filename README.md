# Festival Playlist Generator
Get ready for your next festival or concert by listening to the songs your favorite artists are most likely to perform. This app helps you create Spotify playlists based on their most recent setlists.

Using actual data from [setlist.fm](https://www.setlist.fm) and the [Spotify Web API](https://developer.spotify.com/), you can generate playlists in two ways: either a single combined playlist or one per artist. Choose to include the most frequently played songs or all unique songs from their latest shows.

---

## Features

* Fetch real setlists from setlist.fm using artist MusicBrainz IDs (MBIDs)
* Choose between most common or all unique songs from each artist
* Create a single Spotify playlist for all artists or one playlist per artist
* Automatically removes duplicate songs in combined playlists

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/festival-playlist-generator.git
cd festival-playlist-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your `.env` file

Create a `.env` file in the root directory of the project with the following contents:

```env
# setlist.fm
SETLISTFM_API_KEY=your_setlistfm_api_key
USER_AGENT=your_email_or_app_name

# Spotify
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

#### Getting API Keys

##### setlist.fm

* Sign up for an account on [https://www.setlist.fm](https://www.setlist.fm).
* Request an API key from [https://www.setlist.fm/settings/api](https://www.setlist.fm/settings/api).
* Use your registered email as `USER_AGENT`.

##### Spotify

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Create a new app.
      - **App name**: Whatever you want
      - **App description**: Whatever you want
      - **Redirect URIs**: `http://127.0.0.1:8888/callback` unless you have something more fancy
      - **Which API/SDKs are you planning to use?**: You only need `Web API`
4. Copy the **Client ID** and **Client Secret** into your `.env` file.

---

## Add Artist MBIDs

Each artist must have a **MusicBrainz ID (MBID)** to fetch their setlists.

In `setlist_api/mbids.py`, add entries like this:

```python
artist_mbid = {
    "Muse": "9c9f1380-2516-4fc9-a3e6-f9f61941d090",
    "Avenged Sevenfold": "24e1b53c-3085-4581-8472-0b0088d2508c",
    "Green Day": "084308bd-1654-436f-ba03-df6697104e19"
}
```

To find MBIDs:

* Visit [https://musicbrainz.org](https://musicbrainz.org)
* Search for the artist
* Copy the UUID from the artist's page URL (e.g., `https://musicbrainz.org/artist/9c9f1380-2516-4fc9-a3e6-f9f61941d090`)

---

## Project Structure

```
.
├── main.py                         # Entry point of the app
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
├── setlist_api/                    # Fetch setlists and cache them
│   └── ...
├── playlist_generator/            # Generate playlists from cached setlists
│   └── ...
├── spotify_api/                   # Spotify playlist creation logic
│   └── ...
```

---

## Configuration

Edit the variables at the top of `main.py`:

```python
artists = ["Muse", "Avenged Sevenfold", "Green Day"]
songs_per_artist = 15
use_unique_songs = False              # Use only most frequent songs
playlist_name = "Tons of Rock 2025"
one_big_playlist = True              # Set to False for one playlist per artist
```

---

## ▶Run the app

Once everything is configured:

```bash
python main.py
```

You'll be prompted to log in to Spotify via your browser (once), and then the playlists will be created in your account.

---

## Caching

* Artist setlists are stored in `setlist_api/setlist_cache/`.
* These files are used to avoid repeatedly calling the API.

---

## Example Output

```bash
Creating playlist: 'Tons of Rock 2025' with 42 songs
Playlist created successfully!
```

---

## Notes

* Duplicate songs across artists are removed in combined playlists.
* Playlist creation is rate-limited by the Spotify API; avoid making too many playlists quickly.
* If a song isn’t found on Spotify (e.g., rare live versions), it will be skipped.

---

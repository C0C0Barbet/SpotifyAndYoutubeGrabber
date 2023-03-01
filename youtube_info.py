import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# This file will receive the YouTube link, parse it, and return the first Spotify link it finds


def get_youtube_info(link, client_id, client_secret):
    # Use this request to retreive json info about link
    base_url = "https://noembed.com/embed?url="
    new_url = base_url + link
    response = requests.get(new_url)

    # Retrieve and parse json
    returned_json = response.json()

    # Store the title of the YouTube video, we will search spotify for this
    video_title = returned_json.get("title")

    # Setup spotipy
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Search for track
    results = spot.search(q=video_title, type='track', limit=1)

    # For the found track, return the formulated Spotify URL
    for track in results['tracks']['items']:
        track_id = track['uri'].split(':')[-1]
        spotify_url = f'https://open.spotify.com/track/{track_id}'
        return spotify_url

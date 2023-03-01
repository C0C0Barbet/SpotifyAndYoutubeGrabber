import spotipy
from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyClientCredentials

# This file will receive the Spotify link, parse it, and return the first YouTube link it finds


def get_spotify_info(link, client_id, client_secret, youtube_dev_key):
    # Setup spotipy
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get track info for passed Spotify url
    track_info = spot.track(link)

    # Extract the track title and artist name from the API response
    track_title = track_info['name']
    artist_name = track_info['artists'][0]['name']

    # Setup YouTube Data API
    youtube = build('youtube', 'v3', developerKey=youtube_dev_key)

    # Define the search query and parameters
    query = track_title, ' by ', artist_name
    max_results = 1

    # Call the search.list method to execute the search
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=max_results
    ).execute()

    # Extract the video IDs and titles from the search results
    for item in search_response['items']:
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url

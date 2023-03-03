import spotipy
import googleapiclient.discovery
from spotipy.oauth2 import SpotifyClientCredentials

# This file will receive the Spotify link, parse it, and return the first YouTube link it finds


def get_spotify_info(track_info, youtube_dev_key):

    # Extract the track title and artist name from the API response
    track_title = track_info['name']
    artist_name = track_info['artists'][0]['name']

    # Setup YouTube Data API
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=youtube_dev_key)

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

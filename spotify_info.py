import configparser
import spotipy
from googleapiclient.discovery import build
from spotipy.oauth2 import SpotifyClientCredentials

config = configparser.ConfigParser()
config.read('config.cfg')
client_id = config.get('SPOTIFY', 'SPOTIFY_CLIENT_ID')
client_secret = config.get('SPOTIFY', 'SPOTIFY_CLIENT_SECRET')

youtube_dev_key = config.get('YOUTUBE', 'YOUTUBE_CLIENT_ID')


client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_spotify_info(link):
    track_info = sp.track(link)

    # Extract the track title and artist name from the API response
    track_title = track_info['name']
    artist_name = track_info['artists'][0]['name']
    print(f'{track_title} by: {artist_name}')
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
    videos = []
    for item in search_response['items']:
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url

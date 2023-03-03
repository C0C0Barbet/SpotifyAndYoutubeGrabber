import configparser
import discord
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import os
import spotipy
from spotipy import SpotifyClientCredentials
from link_checker import check_link_type
from youtube_info import get_youtube_info
from spotify_info import get_spotify_info

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Initialize the config file
config = configparser.ConfigParser()
config.read('config.cfg')

# Set all the key variables needed right away
client_id = config.get('SPOTIFY', 'SPOTIFY_CLIENT_ID')
client_secret = config.get('SPOTIFY', 'SPOTIFY_CLIENT_SECRET')
youtube_dev_key = config.get('YOUTUBE', 'YOUTUBE_CLIENT_ID')
google_dev_id = config.get('GOOGLE', 'OAUTH_CLIENT_ID')
google_dev_secret = config.get('GOOGLE', 'OAUTH_CLIENT_SECRET')
bot_token = config.get('DISCORD', 'DISCORD_TOKEN')

# Get the absolute path to the client secrets file
client_secrets_file_path = os.path.abspath("client_secrets.json")

# Define the scopes for the YouTube Data API
scopes = ['https://www.googleapis.com/auth/youtube']

# Load the OAuth2 credentials from a file
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    client_secrets_file_path, scopes=scopes,
    redirect_uri='https://www.colinburgess.dev')


# Generate the authorization URL
authorization_url, state = flow.authorization_url(
    access_type='offline', include_granted_scopes='true')

print(f'Please go to this URL to authorize the application: {authorization_url}')
authorization_response = input('Enter the full authorization code: ')

# Fetch the OAuth2 tokens using the authorization code
flow.fetch_token(authorization_response=authorization_response)

# Create a YouTube API client object using the authorized credentials
youtube = googleapiclient.discovery.build('youtube', 'v3', credentials=flow.credentials)

# Use the client to perform API requests
request = youtube.playlists().list(
    part='id,snippet',
    mine=True
)
response = request.execute()
print(response)

# Setup spotipy
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
spot = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_playlist_id(youtube, playlist_name):
    # Call the playlists().list method to retrieve the list of playlists
    playlists_response = youtube.playlists().list(part='snippet', mine=True).execute()

    # Loop through the list of playlists to find one with matching name
    for playlist in playlists_response['items']:
        if playlist['snippet']['title'] == playlist_name:
            # Return the playlist ID if a match is found
            return playlist['id']

    # If no matching playlist is found, create a new playlist with the specified name
    new_playlist = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': playlist_name
            },
            'status': {
                'privacyStatus': 'private'
            }
        }
    ).execute()

    # Return the ID of the newly created playlist
    return new_playlist['id']


def create_playlist(youtube, title):
    # Call the APIs playlists.insert method to create a new playlist with the specified title
    request = youtube.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': title,
                'description': 'This is a test playlist created by my bot.'
            },
            'status': {
                'privacyStatus': 'private'
            }
        }
    )
    response = request.execute()
    # Return the ID of the newly created playlist
    return response['id']


def run_discord_bot():
    # Initialize the bots settings.
    # Spotify&YouTubeGrabber only needs access to messages really.
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    # Run this when the bot is initialized
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

        # Use server name as playlist name
        playlist_name = str(client.guilds[0].name)
        playlist_id = get_playlist_id(youtube, playlist_name)
        if not playlist_id:
            # Playlist not found, create a new one
            playlist_id = create_playlist(youtube, playlist_name)

        print(f'Using playlist {playlist_name} with ID {playlist_id}.')

    # When a message is sent, run the function
    @client.event
    async def on_message(message):
        # Store channel name to return message to
        channel = str(message.channel.name)

        # Store user and message for now, maybe do something with it later on
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        print(f'{username}: {user_message} ({channel})')

        # This is apparently a check to prevent infinite loops
        if message.author == client.user:
            return

        # This function will return 'Spotify', 'YouTube', or 'No Link' depending on what was sent
        type_of_input = check_link_type(user_message)
        if type_of_input == "Spotify":
            # Get track info for passed Spotify url
            track_info = spot.track(user_message)
            search_string = get_spotify_info(track_info, youtube_dev_key)
            await message.channel.send(search_string)
        elif type_of_input == "YouTube":
            search_string = get_youtube_info(user_message, client_id, client_secret)
            await message.channel.send(search_string)
        else:
            print("No URLs.")

    # Lastly, run the bot
    client.run(bot_token)

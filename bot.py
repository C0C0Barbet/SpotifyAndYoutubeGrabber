import configparser
import discord
from link_checker import check_link_type
from youtube_info import get_youtube_info
from spotify_info import get_spotify_info

# Initialize the config file
config = configparser.ConfigParser()
config.read('config.cfg')

# Set all the key variables needed right away
client_id = config.get('SPOTIFY', 'SPOTIFY_CLIENT_ID')
client_secret = config.get('SPOTIFY', 'SPOTIFY_CLIENT_SECRET')
youtube_dev_key = config.get('YOUTUBE', 'YOUTUBE_CLIENT_ID')
bot_token = config.get('DISCORD', 'DISCORD_TOKEN')


def run_discord_bot():
    # Initialize the bots settings.
    # Spotify&YoutubeGrabber only needs access to messages really.
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    # Run this when the bot is initialized
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

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
            search_string = get_spotify_info(user_message, client_id, client_secret, youtube_dev_key)
            await message.channel.send(search_string)
        elif type_of_input == "YouTube":
            search_string = get_youtube_info(user_message, client_id, client_secret)
            await message.channel.send(search_string)
        else:
            print("No URLs.")

    # Lastly, run the bot
    client.run(bot_token)

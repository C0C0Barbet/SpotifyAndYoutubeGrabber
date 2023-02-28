import configparser
import discord
from link_checker import check_link_type
from youtube_info import get_youtube_info
from spotify_info import get_spotify_info

config = configparser.ConfigParser()
config.read('config.cfg')


def run_discord_bot():
    bot_token = config.get('DISCORD', 'DISCORD_TOKEN')
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        channel = str(message.channel.name)

        if channel == "odeon":
            username = str(message.author).split('#')[0]
            user_message = str(message.content)
            print(f'{username}: {user_message} ({channel})')

            if message.author == client.user:
                return

            type_of_input = check_link_type(user_message)
            if type_of_input == "Spotify":
                search_string = get_spotify_info(user_message)
                await message.channel.send(search_string)
            elif type_of_input == "YouTube":
                search_string = get_youtube_info(user_message)
                await message.channel.send(search_string)
            else:
                print("No URLs.")

    client.run(bot_token)

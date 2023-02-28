import discord
import os
from dotenv import load_dotenv
from link_checker import check_link_type

load_dotenv()


def run_discord_bot():
    bot_token = os.getenv('DISCORD_TOKEN')
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
                print(f"Detected Spotify link: {user_message}")
                await message.channel.send('That\'s a Spotify link!')
            elif type_of_input == "YouTube":
                print(f"Detected YouTube link: {user_message}")
                await message.channel.send('That\'s a YouTube link!')
            else:
                print("No URLs.")

    client.run(bot_token)

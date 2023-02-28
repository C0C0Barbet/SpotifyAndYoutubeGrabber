from googleapiclient.discovery import build
import os

# Set up the API client
api_key = os.environ.get("YOUTUBE_API_KEY")  # Replace with your own API key
youtube = build("youtube", "v3", developerKey=api_key)

# Call the API to search for videos with the keyword "python"
search_response = youtube.search().list(
    q="python",
    type="video",
    part="id,snippet",
    maxResults=10
).execute()

# Print the title of each video in the search results
for search_result in search_response.get("items", []):
    print(f'Title: {search_result["snippet"]["title"]}')


def get_youtube_info(link):
    print(link)

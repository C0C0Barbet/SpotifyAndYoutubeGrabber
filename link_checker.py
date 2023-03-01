import re

# This file will take in the URLs entered to check if they're a Spotify or YouTube link. If neither than the
# program will just return 'No Link', doing nothing


def check_link_type(link):
    # Regular expression pattern to match Spotify links
    spotify_pattern = r'[\bhttps://open.\b]*spotify[\b.com\b]*[/:]*track[/:]*[A-Za-z0-9?=]+'
    # Regular expression pattern to match YouTube links
    youtube_pattern = r'^(?:https?://)?(?:www\.)?(?:m\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}$'

    if re.match(spotify_pattern, link):
        return "Spotify"
    elif re.match(youtube_pattern, link):
        return "YouTube"
    else:
        return "No Link"

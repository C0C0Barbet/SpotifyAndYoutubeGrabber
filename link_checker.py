import re


def check_link_type(link):
    # Regular expression pattern to match Spotify links
    spotify_pattern = r'^https?://(?:open\.spotify\.com|spotify|spoti\.fi)\.[a-z]+(?:[/\w]+)+$'
    # Regular expression pattern to match YouTube links
    youtube_pattern = r'^(?:https?://)?(?:www\.)?(?:m\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}$'

    if re.match(spotify_pattern, link):
        return "Spotify"
    elif re.match(youtube_pattern, link):
        return "YouTube"
    else:
        return "No Link"

import requests

base_url = "https://noembed.com/embed?url="


def get_youtube_info(link):
    new_url = base_url + link
    response = requests.get(new_url)
    returned_json = response.json()
    return returned_json.get("title")

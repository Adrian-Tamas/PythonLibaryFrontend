import requests

from configuration import backend_url


def get_all_books():
    response = requests.get(url=f"{backend_url}/books")
    return response.json()

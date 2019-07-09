import requests

from configuration import backend_url


def get_all_books():
    response = requests.get(url=f"{backend_url}/books")
    return response.json()


def get_all_users():
    response = requests.get(url=f"{backend_url}/users")
    return response.json()


def get_all_reservations():
    response = requests.get(url=f"{backend_url}/reservations")
    return response.json()

import json

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


def create_book(name, author):
    book = {
        "name": name,
        "author": author
    }
    return requests.post(url=f"{backend_url}/books", data=json.dumps(book))


def get_book(book_id):
    return requests.get(url=f"{backend_url}/books/{book_id}")


def edit_book(book_id, name, author):
    book = {
        "name": name,
        "author": author
    }
    return requests.put(url=f"{backend_url}/books/{book_id}", data=json.dumps(book))

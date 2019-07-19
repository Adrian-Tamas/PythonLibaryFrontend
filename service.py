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


def create_book(name, author, description=None, cover=None):
    book = {
        "name": name,
        "author": author,
        "description": description,
        "cover": cover
    }
    return requests.post(url=f"{backend_url}/books", data=json.dumps(book))


def get_book(book_id):
    return requests.get(url=f"{backend_url}/books/{book_id}")


def edit_book(book_id, name, author, description=None, cover=None):
    book = {
        "name": name,
        "author": author,
        "description": description,
        "cover": cover
    }
    return requests.put(url=f"{backend_url}/books/{book_id}", data=json.dumps(book))


def delete_book(book_id):
    return requests.delete(url=f"{backend_url}/books/{book_id}")


def delete_user(user_id):
    return requests.delete(url=f"{backend_url}/users/{user_id}")


def create_user(first_name, last_name, email):
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }
    return requests.post(url=f"{backend_url}/users", data=json.dumps(user))


def get_user(user_id):
    return requests.get(url=f"{backend_url}/users/{user_id}")


def edit_user(user_id, first_name, last_name, email):
    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }
    return requests.put(url=f"{backend_url}/users/{user_id}", data=json.dumps(user))


def create_reservation(book_id, user_id, reservation_date, reservation_expiration_date):
    reservation = {
        "book_id": book_id,
        "user_id": user_id,
        "reservation_date": str(reservation_date),
        "reservation_expiration_date": str(reservation_expiration_date)
    }
    return requests.post(url=f"{backend_url}/reservations", data=json.dumps(reservation))


def get_reservation(user_id, book_id):
    return requests.get(url=f"{backend_url}/reservations/user/{user_id}/book/{book_id}")


def update_reservation(user_id, book_id, reservation_date, reservation_expiration_date):
    reservation = {
        "book_id": book_id,
        "user_id": user_id,
        "reservation_date": str(reservation_date),
        "reservation_expiration_date": str(reservation_expiration_date)
    }
    return requests.put(url=f"{backend_url}/reservations/user/{user_id}/book/{book_id}", data=json.dumps(reservation))


def delete_reservation(user_id, book_id):
    return requests.delete(url=f"{backend_url}/reservations/user/{user_id}/book/{book_id}")

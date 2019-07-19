import datetime
import json

from flask import Flask, render_template, flash, url_for, redirect, request
from configuration import backend_url
from forms.book_form import CreateBookForm, EditBookForm
from forms.user_form import CreateUserForm, EditUserForm
from forms.reservation_form import CreateReservationForm, EditReservationForm

import service

app = Flask("LibraryFrontend")
app.config['SECRET_KEY'] = 'c6852762e4fb8297c336fb03ce0b67bd'


@app.template_filter("to_json")
def to_json(dictionary):
    return json.dumps(dictionary)


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("books"))


@app.route("/books", methods=["GET"])
def books():
    # flash("My error text1", "danger")
    # flash("Good", "success")
    all_books = service.get_all_books()
    return render_template("books.html", all_books=all_books, title="Books")


@app.route("/books/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    response = service.get_book(book_id)
    if response.ok:
        book = response.json()
    else:
        flash("There was an error getting the book details", "danger")
        return redirect(url_for("books"))
    form = EditBookForm()
    if request.method == "POST":
        if form.validate_on_submit():
            response = service.edit_book(book_id=form.id.data,
                                         name=form.name.data,
                                         author=form.author.data,
                                         description=form.description.data,
                                         cover=form.cover.data)
            if response.ok:
                flash(f"Book '{form.name.data}' was successfully saved", "success")
                return redirect(url_for("books"))
            else:
                flash(f"There was an error saving the book because {response.text}", "danger")
        else:
            flash("An error has occurred! Please fix all errors and try again.", "danger")
    else:
        form.id.data = book["id"]
        form.name.data = book["name"]
        form.author.data = book["author"]
        form.description.data = book.get("description")
        form.cover.data = book.get("cover")
    return render_template("edit_book.html", title="Edit Book", form=form, book=book)


@app.route("/books/create", methods=["GET", "POST"])
def create_book():
    form = CreateBookForm()
    if request.method == "POST":
        if form.validate_on_submit():
            response = service.create_book(name=form.name.data,
                                           author=form.author.data,
                                           description=form.description.data,
                                           cover=form.cover.data)
            if response.ok:
                flash(f"Book '{form.name.data}' was successfully saved", "success")
                return redirect(url_for("books"))
            else:
                flash(f"There was an error saving the book because {response.text}", "danger")
        else:
            flash("An error has occurred! Please fix all errors and try again.", "danger")
    return render_template("create_book.html", title="Create Book", form=form)


@app.route("/books/delete/<book_id>", methods=["POST"])
def delete_book(book_id):
    response = service.delete_book(book_id=book_id)
    if response.ok:
        flash(f"Book with id: {book_id} has been successfully deleted!", "success")
    else:
        flash(f"There was a problem deleting the book. Please try again!", "danger")
    return redirect(url_for("books"))


@app.route("/users", methods=["GET"])
def users():
    all_users = service.get_all_users()
    return render_template("users.html", all_users=all_users, title="Users")


@app.route("/users/create", methods=["GET", "POST"])
def create_user():
    form = CreateUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            response = service.create_user(first_name=form.first_name.data,
                                           last_name=form.last_name.data,
                                           email=form.email.data)
            if response.ok:
                flash(f"User with name {form.first_name.data} {form.last_name.data} was created successfully", "success")
                return redirect(url_for("users"))
            else:
                flash(f"There was an error saving the user because: {response.text}. Please try again!", "danger")
        else:
            flash(f"There was an error saving the user. Please fix all issues and try again!", "danger")
    return render_template("create_user.html", title="Create User", form=form)


@app.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    response = service.get_user(user_id=user_id)
    if response.ok:
        user = response.json()
    else:
        flash(f"Unable to retrieve user by user id: {user_id}", "danger")
        return redirect(url_for("users"))
    form = EditUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            response = service.edit_user(user_id=form.id.data,
                                         first_name=form.first_name.data,
                                         last_name=form.last_name.data,
                                         email=form.email.data)
            if response.ok:
                flash(f"User with id: {user_id} was edited successfully", "success")
                return redirect(url_for("users"))
            else:
                flash(f"There was an error saving the user because {response.text}", "danger")
        else:
            flash("There was an error editing the user", "danger")
    else:
        form.first_name.data = user["first_name"]
        form.last_name.data = user["last_name"]
        form.id.data = user["id"]
        form.email.data = user["email"]
    return render_template("edit_user.html", title="Edit User", form=form)


@app.route("/users/delete/<user_id>", methods=["POST"])
def delete_user(user_id):
    response = service.delete_user(user_id=user_id)
    if response.ok:
        flash(f"User with id: {user_id} has been successfully deleted!", "success")
    else:
        flash(f"There was a problem deleting the user because {response.text}. Please try again!", "danger")
    return redirect(url_for("users"))


@app.route("/reservations", methods=["GET"])
def reservations():
    all_reservations = service.get_all_reservations()
    return render_template("reservations.html", all_reservations=all_reservations, title="Reservations")


@app.route("/reservations/create", methods=["GET", "POST"])
def create_reservation():
    all_users = service.get_all_users()
    all_books = service.get_all_books()
    all_reservations = service.get_all_reservations()
    for book in all_books:
        for reservation in all_reservations[:]:
            if book == reservation["book"]:
                all_books.remove(book)
                break

    book_names = [(book["id"], book["name"]) for book in all_books]
    user_names = [(user["id"], f"{user['first_name']} {user['last_name']}") for user in all_users]

    form = CreateReservationForm()
    form.user.choices = user_names
    form.book.choices = book_names
    if request.method == "POST":
        if form.validate_on_submit():
            response = service.create_reservation(book_id=form.book.data,
                                                  user_id=form.user.data,
                                                  reservation_date=form.reservation_date.data,
                                                  reservation_expiration_date=form.reservation_expiration_date.data)
            if response.ok:
                flash("Reservation was successfully saved", "success")
                return redirect(url_for("reservations"))
            else:
                flash(f"There was a problem saving the reservation because {response.text}. Please try again!", "danger")
        else:
            flash("There was an error saving the reservation", "danger")
    return render_template("create_reservation.html", form=form, title="Create Reservation")


@app.route("/reservations/user/<user_id>/book/<book_id>", methods=["GET", "POST"])
def edit_reservation(user_id, book_id):
    form = EditReservationForm()
    response = service.get_reservation(user_id=user_id, book_id=book_id)
    if response.ok:
        reservation = response.json()
        if request.method == "POST":
            if form.validate_on_submit():
                response = service.update_reservation(user_id=user_id,
                                                      book_id=book_id,
                                                      reservation_date=form.reservation_date.data,
                                                      reservation_expiration_date=form.reservation_expiration_date.data)
                if response.ok:
                    flash("Reservation was saved successfully", "success")
                    return redirect(url_for("reservations"))
                else:
                    flash("There was an error editing the reservation. Please fix the errors and try again", "danger")
        else:
            form.book.data = reservation["book"]["name"]
            user = reservation["user"]
            form.user.data = f"{user['first_name']} {user['last_name']}"
            form.reservation_date.data = datetime.datetime.strptime(reservation["reservation_date"], "%Y-%m-%d")
            if reservation["reservation_expiration_date"]:
                form.reservation_expiration_date.data = datetime.datetime.strptime(reservation["reservation_expiration_date"], "%Y-%m-%d")
    else:
        flash("There was an error editing the reservation. Please try again", "danger")
        return redirect(url_for("reservations"))
    return render_template("edit_reservation.html", form=form, title="Edit Reservation")


@app.route("/reservations/delete/user/<user_id>/book/<book_id>", methods=["POST"])
def delete_reservation(user_id, book_id):
    response = service.delete_reservation(user_id=user_id, book_id=book_id)
    if response.ok:
        flash(f"Reservation for user with id: {user_id} and book with id: "
              f"{book_id} has been successfully deleted!", "success")
    else:
        flash(f"There was a problem deleting the reservation because {response.text}. Please try again!", "danger")
    return redirect(url_for("reservations"))


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="127.0.0.1", port=50001, debug="True")

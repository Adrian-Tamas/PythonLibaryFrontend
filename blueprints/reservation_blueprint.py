import datetime

from flask import Blueprint, render_template, flash, url_for, redirect, request

from forms.reservation_form import CreateReservationForm, EditReservationForm

import service

reservations = Blueprint("reservations", __name__)


@reservations.route("/reservations", methods=["GET"])
def get_all_reservations():
    all_reservations = service.get_all_reservations()
    return render_template("reservations.html", all_reservations=all_reservations, title="Reservations")


@reservations.route("/reservations/create", methods=["GET", "POST"])
def create_reservation():
    all_users = service.get_all_users()
    all_existing_books = service.get_all_books()
    all_reservations = service.get_all_reservations()
    all_books = [book for book in all_existing_books
                 if book not in [reservation["book"] for reservation in all_reservations]]

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
                return redirect(url_for("reservations.get_all_reservations"))
            else:
                flash(f"There was a problem saving the reservation because {response.text}. Please try again!", "danger")
        else:
            flash("There was an error saving the reservation", "danger")
    return render_template("create_reservation.html", form=form, title="Create Reservation")


@reservations.route("/reservations/user/<user_id>/book/<book_id>", methods=["GET", "POST"])
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
                    return redirect(url_for("reservations.get_all_reservations"))
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
        return redirect(url_for("reservations.get_all_reservations"))
    return render_template("edit_reservation.html", form=form, title="Edit Reservation")


@reservations.route("/reservations/delete/user/<user_id>/book/<book_id>", methods=["POST"])
def delete_reservation(user_id, book_id):
    response = service.delete_reservation(user_id=user_id, book_id=book_id)
    if response.ok:
        flash(f"Reservation for user with id: {user_id} and book with id: "
              f"{book_id} has been successfully deleted!", "success")
    else:
        flash(f"There was a problem deleting the reservation because {response.text}. Please try again!", "danger")
    return redirect(url_for("reservations.get_all_reservations"))

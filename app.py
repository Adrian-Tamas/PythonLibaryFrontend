from flask import Flask, render_template, flash, url_for
from configuration import backend_url
from service import get_all_books, get_all_users, get_all_reservations

app = Flask("LibraryFrontend")
app.config['SECRET_KEY'] = 'top secret!'


@app.route("/", methods=["GET"])
@app.route("/books", methods=["GET"])
def books():
    # flash("My error text1", "danger")
    # flash("Good", "success")
    all_books = get_all_books()
    return render_template("books.html", all_books=all_books, title="Books")


@app.route("/users", methods=["GET"])
def users():
    all_users = get_all_users()
    return render_template("users.html", all_users=all_users, title="Users")


@app.route("/reservations", methods=["GET"])
def reservations():
    all_reservations = get_all_reservations()
    return render_template("reservations.html", all_reservations=all_reservations, title="Reservations")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=50001, debug="True")

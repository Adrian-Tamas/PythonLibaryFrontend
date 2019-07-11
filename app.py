from flask import Flask, render_template, flash, url_for, redirect, request
from configuration import backend_url
from forms.book_form import CreateBookForm, EditBookForm

import service

app = Flask("LibraryFrontend")
app.config['SECRET_KEY'] = 'c6852762e4fb8297c336fb03ce0b67bd'


@app.route("/", methods=["GET"])
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
            response = service.edit_book(book_id=form.id.data, name=form.name.data, author=form.author.data)
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
    return render_template("edit_book.html", title="Edit Book", form=form, book=book)


@app.route("/books/create", methods=["GET", "POST"])
def create_book():
    form = CreateBookForm()
    if request.method == "POST":
        if form.validate_on_submit():
            response = service.create_book(name=form.name.data, author=form.author.data)
            if response.ok:
                flash(f"Book '{form.name.data}' was successfully saved", "success")
                return redirect(url_for("books"))
            else:
                flash(f"There was an error saving the book because {response.text}", "danger")
        else:
            flash("An error has occurred! Please fix all errors and try again.", "danger")
    return render_template("create_book.html", title="Create Book", form=form)


@app.route("/users", methods=["GET"])
def users():
    all_users = service.get_all_users()
    return render_template("users.html", all_users=all_users, title="Users")


@app.route("/reservations", methods=["GET"])
def reservations():
    all_reservations = service.get_all_reservations()
    return render_template("reservations.html", all_reservations=all_reservations, title="Reservations")


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="127.0.0.1", port=50001, debug="True")

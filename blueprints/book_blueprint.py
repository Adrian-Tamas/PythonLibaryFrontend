from flask import Blueprint, render_template, flash, url_for, redirect, request

from forms.book_form import CreateBookForm, EditBookForm

import service

books = Blueprint("books", __name__)


@books.route("/books", methods=["GET"])
def get_all_books():
    # flash("My error text1", "danger")
    # flash("Good", "success")
    all_books = service.get_all_books()
    return render_template("books.html", all_books=all_books, title="Books")


@books.route("/books/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    response = service.get_book(book_id)
    if response.ok:
        book = response.json()
    else:
        flash("There was an error getting the book details", "danger")
        return redirect(url_for("books.get_all_books"))
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
                return redirect(url_for("books.get_all_books"))
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


@books.route("/books/create", methods=["GET", "POST"])
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
                return redirect(url_for("books.get_all_books"))
            else:
                flash(f"There was an error saving the book because {response.text}", "danger")
        else:
            flash("An error has occurred! Please fix all errors and try again.", "danger")
    return render_template("create_book.html", title="Create Book", form=form)


@books.route("/books/delete/<book_id>", methods=["POST"])
def delete_book(book_id):
    response = service.delete_book(book_id=book_id)
    if response.ok:
        flash(f"Book with id: {book_id} has been successfully deleted!", "success")
    else:
        flash(f"There was a problem deleting the book. Please try again!", "danger")
    return redirect(url_for("books.get_all_books"))

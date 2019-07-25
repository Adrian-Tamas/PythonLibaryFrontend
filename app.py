import json

from flask import Flask, render_template, flash, url_for, redirect
from blueprints.book_blueprint import books
from blueprints.user_blueprint import users
from blueprints.reservation_blueprint import reservations

app = Flask("LibraryFrontend")
app.config['SECRET_KEY'] = 'c6852762e4fb8297c336fb03ce0b67bd'


app.register_blueprint(books)
app.register_blueprint(users)
app.register_blueprint(reservations)


@app.template_filter("to_json")
def to_json(dictionary):
    return json.dumps(dictionary)


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("books.get_all_books"))


@app.errorhandler(404)
def not_found(error):
    flash(f"There was a problem finding the page you wanted", "danger")
    return render_template("404.html", title="Page not found"), 404


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="127.0.0.1", port=50001, debug="True")

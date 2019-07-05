from flask import Flask, render_template, flash
from configuration import backend_url
from service import get_all_books

app = Flask("LibraryFrontend")
app.config['SECRET_KEY'] = 'top secret!'


# TODO: integrate bootstrap not JS
@app.route("/", methods=["GET"])
def index():
    # flash("My error text1")
    all_books = get_all_books()
    return render_template("index.html", all_books=all_books)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=50001, debug="True")

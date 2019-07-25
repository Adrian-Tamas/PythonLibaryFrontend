from flask import Blueprint, render_template, flash, url_for, redirect, request

from forms.user_form import CreateUserForm, EditUserForm

import service

users = Blueprint("users", __name__)


@users.route("/users", methods=["GET"])
def get_all_users():
    all_users = service.get_all_users()
    return render_template("users.html", all_users=all_users, title="Users")


@users.route("/users/create", methods=["GET", "POST"])
def create_user():
    form = CreateUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            response = service.create_user(first_name=form.first_name.data,
                                           last_name=form.last_name.data,
                                           email=form.email.data)
            if response.ok:
                flash(f"User with name {form.first_name.data} {form.last_name.data} was created successfully", "success")
                return redirect(url_for("users.get_all_users"))
            else:
                flash(f"There was an error saving the user because: {response.text}. Please try again!", "danger")
        else:
            flash(f"There was an error saving the user. Please fix all issues and try again!", "danger")
    return render_template("create_user.html", title="Create User", form=form)


@users.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    response = service.get_user(user_id=user_id)
    if response.ok:
        user = response.json()
    else:
        flash(f"Unable to retrieve user by user id: {user_id}", "danger")
        return redirect(url_for("users.get_all_users"))
    form = EditUserForm()
    if request.method == "POST":
        if form.validate_on_submit():
            response = service.edit_user(user_id=form.id.data,
                                         first_name=form.first_name.data,
                                         last_name=form.last_name.data,
                                         email=form.email.data)
            if response.ok:
                flash(f"User with id: {user_id} was edited successfully", "success")
                return redirect(url_for("users.get_all_users"))
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


@users.route("/users/delete/<user_id>", methods=["POST"])
def delete_user(user_id):
    response = service.delete_user(user_id=user_id)
    if response.ok:
        flash(f"User with id: {user_id} has been successfully deleted!", "success")
    else:
        flash(f"There was a problem deleting the user because {response.text}. Please try again!", "danger")
    return redirect(url_for("users.get_all_users"))

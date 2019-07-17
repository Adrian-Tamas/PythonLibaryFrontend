from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class CreateUserForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    confirm_email = StringField("Confirm Email", validators=[DataRequired(),
                                                             Email(),
                                                             EqualTo(fieldname="email",
                                                                     message="Emails do not match")])

    save = SubmitField("Create User")


class EditUserForm(FlaskForm):

    id = StringField("User Id")
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2)])

    email = StringField("Email")

    save = SubmitField("Edit User")

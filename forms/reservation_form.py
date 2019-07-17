from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired
from forms.custom_validators import DateGreaterThan


class CreateReservationForm(FlaskForm):
    user = SelectField("User", validators=[InputRequired()])
    book = SelectField("Book", validators=[InputRequired()])
    reservation_date = DateField("Reservation Date", format='%Y-%m-%d', validators=[InputRequired()])
    reservation_expiration_date = DateField("Reservation Expiration Date",
                                            format='%Y-%m-%d',
                                            validators=[DateGreaterThan(fieldname="reservation_date",
                                                                        date_format="%Y-%m-%d")])

    save = SubmitField("Save reservation")


class EditReservationForm(FlaskForm):
    user = StringField("User")
    book = StringField("Book")
    reservation_date = DateField("Reservation Date", format='%Y-%m-%d', validators=[InputRequired()])
    reservation_expiration_date = DateField("Reservation Expiration Date",
                                            format='%Y-%m-%d',
                                            validators=[DateGreaterThan(fieldname="reservation_date",
                                                                        date_format="%Y-%m-%d")])
    save = SubmitField("Edit reservation")

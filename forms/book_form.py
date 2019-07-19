from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CreateBookForm(FlaskForm):

    name = StringField("Book Name", validators=[DataRequired(), Length(min=3)])
    author = StringField("Author Name", validators=[DataRequired(), Length(min=3, max=30)])
    description = TextAreaField("Book Description")
    cover = StringField("Cover Link")

    save = SubmitField("Create Book")


class EditBookForm(FlaskForm):

    id = StringField("Book Id")
    name = StringField("Book Name", validators=[DataRequired(), Length(min=3)])
    author = StringField("Author Name", validators=[DataRequired(), Length(min=3, max=30)])
    description = TextAreaField("Book Description")
    cover = StringField("Cover Link")

    save = SubmitField("Edit Book")

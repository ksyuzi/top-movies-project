from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

# THESE CLASSES CREATE FLASK FORMS FOR ADDING AND EDITING FILMS


class EditFilmForm(FlaskForm):
    new_film_rating = StringField('Your New Rating out of 10', validators=[InputRequired()])
    new_film_review = StringField('Your Review', validators=[InputRequired()])
    submit = SubmitField('Edit')


class AddFilmForm(FlaskForm):
    title = StringField('Film Title', validators=[InputRequired()])
    submit = SubmitField('Add')

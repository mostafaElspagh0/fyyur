from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,AnyOf,URL
from enums import State,Genre
from .validators import genre_validator



class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state',
        validators=[
            DataRequired(),
            AnyOf([state.value for state in State])
        ],
        choices=[(state.value, state.value) for state in State]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), genre_validator()],
        choices=[(genre.value, genre.value) for genre in Genre]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website_link',
        validators=[URL()]
    )
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = TextAreaField('seeking_description')

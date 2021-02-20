from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL
from enums import State, Genre


def genre_validate():
    message = 'Invalid genre value.'
    values = [g.value for g in Genre]

    def _validate(form, field):
        for value in field.data:
            if value not in values:
                raise ValidationError(message)

    return _validate


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


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
        'genres', validators=[DataRequired(), genre_validate()],
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


class ArtistForm(FlaskForm):
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
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired(), genre_validate()],
        choices=[(genre.value, genre.value) for genre in Genre]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

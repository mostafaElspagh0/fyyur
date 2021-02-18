from app import db
from models.CityModel import City
from models.StateModel import State


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.String(500))

    # foreign keys
    city_id = db.Column(db.Integer, db.ForeignKey(f'{City.__tablename__}.id'))
    state_id = db.Column(db.Integer, db.ForeignKey(f'{State.__tablename__}.id'))

    # relations
    shows = db.relationship('Show', backref='artist', lazy=True)

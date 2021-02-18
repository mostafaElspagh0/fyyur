from app import db
from .CityModel import City
from .StateModel import State
from .GenreModel import Genre


artist_genre_table = db.Table('artist_genre_table',
                              db.Column('genre_id', db.Integer, db.ForeignKey(f'{Genre.__tablename__}.id'),
                                        primary_key=True),
                              db.Column('artist_id', db.Integer, db.ForeignKey(f'artists.id'),
                                        primary_key=True)
                              )


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    # foreign keys
    city_id = db.Column(db.Integer, db.ForeignKey(f'{City.__tablename__}.id'))
    state_id = db.Column(db.Integer, db.ForeignKey(f'{State.__tablename__}.id'))

    # relations
    shows = db.relationship('Show', backref='artist', lazy=True)
    genres = db.relationship('Genre', secondary=artist_genre_table, backref=db.backref('artists'))

    def __repr__(self):
        return f'<Artist {self.id}, {self.name}>'
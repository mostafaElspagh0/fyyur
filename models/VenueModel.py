from app import db
from models.StateModel import State
from models.CityModel import City
from models.GenreModel import Genre

venue_genreTable = db.Table('venue_genre_table',
                            db.Column('genre_id', db.Integer, db.ForeignKey(f'{Genre.__tablename__}.id'),
                                      primary_key=True),
                            db.Column('venue_id', db.Integer, db.ForeignKey(f'venues.id'),
                                      primary_key=True)
                            )


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    # foreign keys
    city_id = db.Column(db.Integer, db.ForeignKey(f'{City.__tablename__}.id'))
    state_id = db.Column(db.Integer, db.ForeignKey(f'{State.__tablename__}.id'))

    # relations
    shows = db.relationship('Show', backref='venue', lazy=True)
    genres = db.relationship('Genre', secondary=venue_genreTable, backref=db.backref('venues'))

    def __repr__(self):
        return f'<Venue {self.id}, {self.name}>'

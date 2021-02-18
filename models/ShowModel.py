from app import db
from .ArtistModel import Artist
from .VenueModel import Venue


class Show(db.Model):
    __tablename__ = "shows"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(f'{Artist.__tablename__}.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey(f'{Venue.__tablename__}.id'))
    start_time = db.Column(db.DateTime)
    duration_inMinutes = db.Column(db.Integer , nullable=False ,default=100)

    def __repr__(self):
        return f'<Show {self.id}, {self.start_time}, {self.duration_inMinutes}>'
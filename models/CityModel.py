from app import db
from .StateModel import State


class City(db.Model):
    __tablename__ = "cities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    # foreign keys
    state_id = db.Column(db.Integer, db.ForeignKey(f'{State.__tablename__}.id'))

    # relations
    venues = db.relationship('Venue', backref='city', lazy=True)

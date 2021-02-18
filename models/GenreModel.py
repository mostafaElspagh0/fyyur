from app import db


class Genre (db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer)
    name = db.Column(db.String(120))
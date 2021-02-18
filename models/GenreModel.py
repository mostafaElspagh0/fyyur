from app import db


class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __repr__(self):
        return f'<Genre {self.id}, {self.name}>'
from app import db

venue_genreTable = db.Table('venue_genre_table',
                            db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id'), primary_key=True),
                            db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
                            )

import sys
from datetime import datetime

from app import (
    app,
    db,
)
from forms import ArtistForm, VenueForm
from models import *
from flask import (
    render_template,
    request,
    abort,
    flash,
    redirect,
    url_for
)


@app.route('/artists')
def artists():
    data = [{
        "id": artist.id,
        "name": artist.name,
    } for artist
        in Artist.query.all()]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get("search_term")
    data = Artist.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(data),
        "data": [{
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": Show.query.with_parent(artist).filter(
                Show.start_time > datetime.now()).count(),
        } for artist in data]
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(int(artist_id))
    if artist is None:
        abort(404)
    past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(
        Show.start_time > datetime.now()).all()
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_image_link": show.venue.image_link,
            "start_time": str(show.start_time)
        })

    upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(
        Show.start_time < datetime.now()).all()
    upcoming_shows = []

    for show in upcoming_shows_query:
        upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "artist_image_link": show.venue.image_link,
            "start_time": str(show.start_time)
        })

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": [genre.name for genre in artist.genres],
        "city": artist.city.name,
        "state": artist.state.name,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    if artist:
        form.name.data = artist.name
        form.city.data = artist.city.name
        form.state.data = artist.state.name
        form.phone.data = artist.phone
        form.genres.data = [genre.name for genre in artist.genres]
        form.facebook_link.data = artist.facebook_link
        form.image_link.data = artist.image_link
        form.website.data = artist.website
        form.seeking_venue.data = artist.seeking_venue
        form.seeking_description.data = artist.seeking_description
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    if not form.validate_on_submit():
        flash('An error occurred. Artist could not be changed.')
        return render_template('pages/home.html')
    error = False
    artist = Artist.query.get(artist_id)
    try:
        artist.name = request.form['name']
        temp_state = State.query.filter(State.name == request.form['state']).one_or_none()
        if temp_state is None:
            temp_state = State(name=request.form['state'])
            db.session.add(temp_state)
        artist.state = temp_state
        temp_city = City.query.filter(City.name == request.form['city']).one_or_none()
        if temp_city is None:
            temp_city = City(name=request.form['city'], state_id=temp_state.id)
            db.session.add(temp_city)
        artist.city = temp_city
        artist.phone = request.form['phone']
        temp_genres = []
        for genre_name in request.form.getlist('genres'):
            genre = Genre.query.filter(Genre.name == genre_name.strip()).one_or_none()
            if genre is not None:
                temp_genres.append(genre)
        artist.genres = temp_genres
        artist.image_link = request.form['image_link']
        artist.facebook_link = request.form['facebook_link']
        artist.website = request.form['website']
        artist.seeking_venue = True if 'seeking_venue' in request.form else False
        artist.seeking_description = request.form['seeking_description']

        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist could not be changed.')
    if not error:
        flash('Artist was successfully updated!')
    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)
    if not form.validate_on_submit():
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        return render_template('pages/home.html')
    error = False
    try:
        artist = Artist()
        artist.name = request.form['name']
        temp_state = State.query.filter(State.name == request.form['state']).one_or_none()
        if temp_state is None:
            temp_state = State(name=request.form['state'])
            db.session.add(temp_state)
        artist.state = temp_state
        temp_city = City.query.filter(City.name == request.form['city']).one_or_none()
        if temp_city is None:
            temp_city = City(name=request.form['city'], state_id=temp_state.id)
            db.session.add(temp_city)
        artist.city = temp_city
        artist.phone = request.form['phone']
        temp_genres = []
        for genre_name in request.form.getlist('genres'):
            genre = Genre.query.filter(Genre.name == genre_name.strip()).one_or_none()
            if genre is not None:
                temp_genres.append(genre)
        artist.genres = temp_genres
        artist.facebook_link = request.form['facebook_link']
        db.session.add(artist)
        db.session.commit()
    except Exception:
        error = True
        print(Exception.__name__)
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        else:
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')

import sys
from datetime import datetime
from forms import VenueForm
from app import (
    app,
    db
)
from models import *
from flask import render_template, request, abort, flash


@app.route('/venues')
def venues():
    data = [{
        "city": city.name,
        "state": city.state.name,
        "venues": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": Show.query.with_parent(venue).filter(
                Show.start_time > datetime.now()).count(),
        } for venue in city.venues]
    } for city in City.query.all()]
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get("search_term")
    data = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
    response = {
        "count": len(data),
        "data": [{
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": Show.query.with_parent(venue).filter(
                Show.start_time > datetime.now()).count(),
        } for venue in data]
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    if venue is None:
        abort(404)
    past_shows = []
    upcoming_shows = []
    now = datetime.now()
    for show in venue.shows:
        artist = Artist
        show_data = {
            "artist_id": show.artist_id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(show.start_time)
        }
        if show.start_time > now:
            upcoming_shows.append(show_data)
        else:
            past_shows.append(show_data)
    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": [genre.name for genre in venue.genres],
        "address": venue.address,
        "city": venue.city.name,
        "state": venue.state.name,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_venue.html', venue=data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm(request.form)
    if not form.validate_on_submit():
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        return render_template('pages/home.html')
    error = False
    try:
        venue = Venue()
        venue.name = request.form['name']
        temp_state = State.query.filter(State.name == request.form['state']).one_or_none()
        if temp_state is None:
            temp_state = State(name=request.form['state'])
            db.session.add(temp_state)
        venue.state = temp_state
        temp_city = City.query.filter(City.name == request.form['city']).one_or_none()
        if temp_city is None:
            temp_city = City(name=request.form['city'], state_id=temp_state.id)
            db.session.add(temp_city)
        venue.city = temp_city
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        temp_genres = []
        for genre_name in request.form.getlist('genres'):
            genre = Genre.query.filter(Genre.name == genre_name.strip()).one_or_none()
            if genre is not None:
                temp_genres.append(genre)
        venue.genres = temp_genres
        venue.facebook_link = request.form['facebook_link']
        venue.website = request.form['website']
        venue.seeking_talent = 'seeking_talent' in request.form.keys()
        venue.seeking_description = request.form['seeking_description']
        db.session.add(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
        else:
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    error = False
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash(f'An error occurred. Venue {venue_id} could not be deleted.')
    if not error:
        flash(f'Venue {venue_id} was successfully deleted.')
    return render_template('pages/home.html')
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)

    if venue:
        form.name.data = venue.name
        form.city.data = venue.city.name
        form.state.data = venue.state.name
        form.phone.data = venue.phone
        form.address.data = venue.address
        form.genres.data = [genre.name for genre in venue.genres]
        form.facebook_link.data = venue.facebook_link
        form.image_link.data = venue.image_link
        form.website.data = venue.website
        form.seeking_talent.data = venue.seeking_talent
        form.seeking_description.data = venue.seeking_description
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False
    venue = Venue.query.get(venue_id)
    form = VenueForm(request.form)
    if not form.validate_on_submit():
        flash(f'An error occurred. Venue could not be changed.')
        return redirect(url_for('show_venue', venue_id=venue_id))
    try:
        venue.name = request.form['name']
        temp_state = State.query.filter(State.name == request.form['state']).one_or_none()
        if temp_state is None:
            temp_state = State(name=request.form['state'])
            db.session.add(temp_state)
        venue.state = temp_state
        temp_city = City.query.filter(City.name == request.form['city']).one_or_none()
        if temp_city is None:
            temp_city = City(name=request.form['city'], state_id=temp_state.id)
            db.session.add(temp_city)
        venue.city = temp_city
        venue.address = request.form['address']
        venue.phone = request.form['phone']
        temp_genres = []
        for genre_name in request.form.getlist('genres'):
            genre = Genre.query.filter(Genre.name == genre_name.strip()).one_or_none()
            if genre is not None:
                temp_genres.append(genre)
        venue.genres = temp_genres
        venue.image_link = request.form['image_link']
        venue.facebook_link = request.form['facebook_link']
        venue.website = request.form['website']
        venue.seeking_talent = True if 'seeking_talent' in request.form else False
        venue.seeking_description = request.form['seeking_description']

        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash(f'An error occurred. Venue could not be changed.')
    if not error:
        flash(f'Venue was successfully updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))

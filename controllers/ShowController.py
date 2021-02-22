import sys
from forms import ShowForm
from app import (
    app,
    db,
)
from models import *
from flask import (
    render_template,
    request,
    flash,
)


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    shows_data = db.session.query(Show).join(Artist).join(Venue).all()
    data = []
    for show in shows_data:
        artist = show.artist
        venue = show.venue
        data.append({
            "venue_id": venue.id,
            "venue_name": venue.name,
            "artist_id": artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": str(show.start_time)
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    error = False
    form = ShowForm(request.form)
    if not form.validate_on_submit():
        flash('An error occurred. Show could not be listed.')
        return render_template('pages/home.html')
    # noinspection PyBroadException
    try:
        artist_id = request.form['artist_id']
        venue_id = request.form['venue_id']
        start_time = request.form['start_time']
        show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
    except Exception:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Show could not be listed.')
    if not error:
        flash('Show was successfully listed')
    return render_template('pages/home.html')

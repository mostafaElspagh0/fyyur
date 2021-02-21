from app import app

from flask import render_template


# bad_request - 400
# unauthorized - 401
# forbidden - 403
# not_found - 404
# server_error - 500
# not_processable - 422
# invalid_method - 405
# duplicate_resource - 409
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

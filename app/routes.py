from flask import current_app as app
from flask.json import jsonify
from app import api


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

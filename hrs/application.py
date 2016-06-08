# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, '')

from flask import Flask, Response, request, jsonify, make_response
from werkzeug.exceptions import default_exceptions, HTTPException

from hrs.models import configure_db
from hrs.api import configure_api


DEFAULT_APPNAME = 'hrs'


class JSONTypeResponse(Response):
    default_mimetype = 'application/json'

    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(JSONTypeResponse, cls).force_type(rv, environ)


def create_app(config=None, app_name=None):

    if app_name is None:
        app_name = DEFAULT_APPNAME

    app = Flask(app_name, static_folder=None)
    app.response_class = JSONTypeResponse

    configure_app(app, config)
    configure_db(app)
    configure_api(app)

    return app


def configure_app(app, config=None):

    if config is not None:
        app.config.from_object(config)
    else:
        try:
            app.config.from_object('localconfig.LocalConfig')
        except ImportError:
            app.config.from_object('hrs.config.DevelopmentConfig')

    @app.after_request
    def add_cors_headers(response):
        if 'Origin' in request.headers:

            a = response.headers.add
            a('Access-Control-Allow-Origin', request.headers['Origin'])
            a('Access-Control-Allow-Credentials', 'true')
            a('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            a('Access-Control-Allow-Methods', 'GET,PUT,PATCH,POST,DELETE')
        return response

    def make_json_error(ex):
        err = {'error': str(ex)}
        if hasattr(ex, 'data') and 'messages' in ex.data:
            err.update({'messages': ex.data['messages']})
        return make_response(err,
                             ex.code if isinstance(ex, HTTPException) else 500)

    for code in default_exceptions.keys():
        app.register_error_handler(code, make_json_error)

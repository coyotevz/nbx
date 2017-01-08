# -*- coding: utf-8 -*-

import locale
import os
from os import path

from flask import Flask, g, request
from flask_principal import Principal, identity_loaded
from nbx.api import configure_api
from nbx.models import User, db

__all__ = ['create_app']

DEFAULT_APPNAME = 'nbx'


def create_app(config=None, app_name=None):

    if app_name is None:
        app_name = DEFAULT_APPNAME

    app = Flask(app_name)

    configure_app(app, config)
    configure_db(app)
    configure_identity(app)

    configure_api(app)

    return app


def configure_app(app, config=None):

    if config is not None:
        app.config.from_object(config)
    else:
        try:
            app.config.from_object('localconfig.LocalConfig')
        except ImportError:
            if os.getenv('DEV') == 'yes':
                app.config.from_object('nbx.config.DevelopmentConfig')
                app.logger.info("Config: Development")
            elif os.getenv('TEST') == 'yes':
                app.config.from_object('nbx.config.TestConfig')
                app.logger.info("Config: Test")
            else:
                app.config.from_object('nbx.config.ProductionConfig')
                app.logger.info("Config: Production")

    @app.after_request
    def add_cors_headers(response):
        if 'Origin' in request.headers:

            a = response.headers.add
            a('Access-Control-Allow-Origin', request.headers['Origin'])
            a('Access-Control-Allow-Credentials', 'true')
            a('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            a('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,HEAD')
            a('Access-Control-Expose-Headers', 'Link,X-Total-Count')
        return response


def configure_db(app):
    db.init_app(app)


def configure_identity(app):

    Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        g.user = User.query.from_identity(identity)

    @app.before_request
    def authenticate():
        g.user = getattr(g.identity, 'user', None)

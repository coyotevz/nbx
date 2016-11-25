# -*- coding: utf-8 -*-

import os
from os import path
import locale
locale.setlocale(locale.LC_ALL, '')

from flask import Flask, g
from flask_assets import Environment, Bundle
from flask_principal import Principal, identity_loaded

from webassets.filter import get_filter

from nbx.views import supplier, product, order, account
from nbx.models import db, User
from nbx.jinjafilters import dateformat_filter, timeago_filter, moneyfmt_filter

__all__ = ['create_app']

DEFAULT_APPNAME = 'nbx'


def create_app(config=None, app_name=None):

    if app_name is None:
        app_name = DEFAULT_APPNAME

    app = Flask(app_name)

    configure_app(app, config)
    configure_jinja2(app)
    configure_webassets(app)
    configure_db(app)
    configure_identity(app)

    configure_blueprints(app)

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


def configure_jinja2(app):
    # Jinja2 extensions
    app.jinja_options['extensions'].extend([
        'jinja2.ext.i18n',
        'jinja2.ext.do',
        'jinja2.ext.loopcontrols',
    ])

    # Jinja2 filters
    app.jinja_env.filters['dateformat'] = dateformat_filter
    app.jinja_env.filters['timeago'] = timeago_filter
    app.jinja_env.filters['moneyfmt'] = moneyfmt_filter


def configure_webassets(app):
    # Fask-Assets
    assets = Environment(app)
    assets_out_dir = app.config.get('ASSETS_OUTPUT_DIR')
    # ensure output directory exists
    if not path.exists(path.join(app.static_folder, assets_out_dir)):
        app.logger.info("Creating assets output folder")
        os.mkdir(path.join(app.static_folder, assets_out_dir))

    # webassets bundles

    jquery_bundle = Bundle(
        'js/libs/jquery-3.1.1.js',
    )

    js_bootstrap_bundle = Bundle(
        'js/bootstrap/transition.js',
        'js/bootstrap/alert.js',
        'js/bootstrap/button.js',
        'js/bootstrap/carousel.js',
        'js/bootstrap/collapse.js',
        'js/bootstrap/dropdown.js',
        'js/bootstrap/modal.js',
        'js/bootstrap/tab.js',
        'js/bootstrap/affix.js',
        'js/bootstrap/scrollspy.js',
        'js/bootstrap/tooltip.js',
        'js/bootstrap/popover.js',
    )

    js_bundle = Bundle(
        jquery_bundle,
        js_bootstrap_bundle,
        filters='jsmin',
        output=path.join(assets_out_dir, 'js_bundle.js')
    )

    scss = get_filter('scss', load_paths=['style'])

    scss_bundle = Bundle(
        'style/master.scss',
        filters=scss,
        output=path.join(assets_out_dir, 'style_bundle.css'),
        depends=('style/*.scss',)
    )

    css_bundle = Bundle(
        scss_bundle,
        filters='autoprefixer, cssmin',
        output=path.join(assets_out_dir, 'css_bundle.css'),
    )

    assets.register('js_bundle', js_bundle)
    assets.register('css_bundle', css_bundle)


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


def configure_blueprints(app):
    app.register_blueprint(supplier, url_prefix='/suppliers')
    app.register_blueprint(product, url_prefix='/products')
    app.register_blueprint(order, url_prefix='/orders')
    app.register_blueprint(account, url_prefix='/accounts')

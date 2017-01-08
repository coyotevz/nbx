# -*- coding: utf-8 -*-

from flask_potion import Api
from .supplier import SupplierResource


def register_resources(api):
    api.add_resource(SupplierResource)


def configure_api(app):
    api = Api(prefix='/api')
    register_resources(api)
    api.init_app(app)

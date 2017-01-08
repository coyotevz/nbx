# -*- coding: utf-8 -*-

from flask_potion import Api
from .supplier import SupplierResource
from .document import DocumentResource


def register_resources(api):
    api.add_resource(SupplierResource)
    api.add_resource(DocumentResource)


def configure_api(app):
    api = Api(prefix='/api')
    register_resources(api)
    api.init_app(app)

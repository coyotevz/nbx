# -*- coding: utf-8 -*-

from flask_potion import Api, ModelResource, fields
from flask_potion.routes import Relation

from nbx.models import Supplier, Document


api = Api(prefix='/api')


class DocumentResource(ModelResource):

    class Meta:
        model = Document
        name = 'documents'

    class Schema:
        supplier = fields.ToOne('suppliers')


class SupplierResource(ModelResource):
    documents = Relation('documents')

    class Meta:
        model = Supplier
        name = 'suppliers'
        exclude_fields = ['entity_type']

    class Schema:
        rz = fields.String(attribute='_name_1')
        name = fields.String(attribute='_name_2')


api.add_resource(DocumentResource)
api.add_resource(SupplierResource)


def configure_api(app):
    api.init_app(app)

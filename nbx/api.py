# -*- coding: utf-8 -*-

from flask_potion import Api, ModelResource, fields
from flask_potion.routes import Relation

from nbx.models import Supplier, Document, Contact


api = Api(prefix='/api')


class DocumentResource(ModelResource):

    class Meta:
        model = Document
        name = 'documents'

    class Schema:
        supplier = fields.ToOne('suppliers')


class ContactResource(ModelResource):

    class Meta:
        model = Contact
        name = 'contacts'
        exclude_fields = ['entity_type']

    class Schema:
        first_name = fields.String(attribute='_name_1')
        last_name = fields.String(attribute='_name_2')
        suppliers = fields.ToMany('suppliers')


class SupplierResource(ModelResource):
    documents = Relation('documents')
    contacts = Relation('contacts')

    class Meta:
        model = Supplier
        name = 'suppliers'
        exclude_fields = ['entity_type']
        include_id = True

    class Schema:
        rz = fields.String(attribute='_name_1')
        name = fields.String(attribute='_name_2')


api.add_resource(DocumentResource)
api.add_resource(ContactResource)
api.add_resource(SupplierResource)


def configure_api(app):
    api.init_app(app)

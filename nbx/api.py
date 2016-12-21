# -*- coding: utf-8 -*-

from flask_potion import Api, ModelResource, fields
from flask_potion.contrib.alchemy.fields import InlineModel
from flask_potion.routes import Relation

from nbx.models import (Address, Bank, BankAccount, Contact, Document,
                        FiscalData, PurchaseOrder, Supplier)

api = Api(prefix='/api')


class DocumentResource(ModelResource):

    class Meta:
        model = Document
        name = 'documents'

    class Schema:
        supplier = fields.ToOne('suppliers')
        supplier_data = InlineModel({
            '$id': fields.Integer(attribute='id'),
            'rz': fields.String(),
        }, model=Supplier, attribute='supplier')
        type = fields.String(io='r')
        short_type = fields.String(io='r')
        full_number = fields.String(io='r')


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
    orders = Relation('orders')

    class Meta:
        model = Supplier
        name = 'suppliers'
        exclude_fields = ['entity_type']
        include_id = True

    class Schema:
        rz = fields.String(attribute='_name_1')
        name = fields.String(attribute='_name_2')
        address = fields.List(InlineModel({
            'street': fields.String(),
            'streetnumber': fields.String(),
            'city': fields.String(),
            'province': fields.String(),
            'zip_code': fields.String(),
            'address_type': fields.String(),
        }, model=Address))
        bank_accounts = fields.List(InlineModel({
            'bank': InlineModel({
                '$id': fields.Integer(attribute='id'),
                'name': fields.String(),
            }, model=Bank),
            'branch': fields.String(),
            'acc_type': fields.String(),
            'number': fields.String(),
            'owner': fields.String(),
            'cbu': fields.String(),
        }, model=BankAccount))
        fiscal_data = InlineModel({
            'cuit': fields.String(),
            'type': fields.String(),
            'iibb': fields.String(),
        }, model=FiscalData)


class OrderResource(ModelResource):

    class Meta:
        model = PurchaseOrder
        name = 'orders'

    class Schema:
        supplier = fields.ToOne('suppliers')
        supplier_data = InlineModel({
            '$id': fields.Integer(attribute='id'),
            'rz': fields.String()
        }, model=Supplier, attribute='supplier')
        status = fields.String()
        method = fields.String()
        full_desc = fields.String(io='r')


api.add_resource(DocumentResource)
api.add_resource(ContactResource)
api.add_resource(OrderResource)
api.add_resource(SupplierResource)


def configure_api(app):
    api.init_app(app)

# -*- coding: utf-8 -*-

#from flask_potion import fields
#
#BankSchema = fields.Object({
#    '$id': fields.Integer(attribute='id'),
#    'name': fields.String(),
#})
#
#BankAccountSchema = fields.Object({
#    'bank': BankSchema,
#    'branch': fields.String(),
#    'acc_type': fields.String(),
#    'number': fields.String(),
#    'owner': fields.String(),
#    'cbu': fields.String(),
#})

from marshmallow import Schema, fields
from nbx.models.bank import BankAccount
from nbx.tonic.resource import Resource


class BankSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    bcra_code = fields.String()
    cuit = fields.String()


class BankAccountResource(Resource):

    class Meta:
        model = BankAccount

    class Schema:
        id = fields.Integer(dump_only=True)
        bank = fields.Nested(BankSchema)

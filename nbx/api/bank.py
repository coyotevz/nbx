# -*- coding: utf-8 -*-

from flask_potion import fields

BankSchema = fields.Object({
    '$id': fields.Integer(attribute='id'),
    'name': fields.String(),
})

BankAccountSchema = fields.Object({
    'bank': BankSchema,
    'branch': fields.String(),
    'acc_type': fields.String(),
    'number': fields.String(),
    'owner': fields.String(),
    'cbu': fields.String(),
})

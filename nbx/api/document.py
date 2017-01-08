# -*- coding: utf-8 -*-

from flask_potion import ModelResource, fields

from nbx.models import Document


DocumentSchema = fields.Object({
    '$id': fields.Integer(attribute='id'),
    'type': fields.String(io='r'),
    'short_type': fields.String(io='r'),
    'full_number': fields.String(io='r'),
    'total': fields.Number(),
    'status': fields.String(),
    'issue_date': fields.Date(),
    'expiration_date': fields.Date(),
    'notes': fields.String()
})


class DocumentResource(ModelResource):

    class Meta:
        model = Document
        name = 'documents'

    class Schema:
        type = fields.String(io='r')
        short_type = fields.String(io='r')
        full_number = fields.String(io='r')

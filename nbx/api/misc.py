# -*- coding: utf-8 -*-

from flask_potion import fields


AddressSchema = fields.Object({
    'street': fields.String(),
    'streetnumber': fields.String(),
    'city': fields.String(),
    'province': fields.String(),
    'zip_code': fields.String(),
    'address_type': fields.String(),
})


EmailSchema = fields.Object({
    'email_type': fields.String(),
    'email': fields.String(),
})


PhoneSchema = fields.Object({
    'phone_type': fields.String(),
    'number': fields.String(),
})


class TimestampMixin(object):

    class Schema:
        created = fields.DateTime(io='r')
        modified = fields.DateTime(io='r')

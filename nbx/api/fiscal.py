# -*- coding: utf-8 -*-

from flask_potion import fields

FiscalDataSchema = fields.Object({
    'cuit': fields.String(),
    'type': fields.String(),
    'iibb': fields.String(),
})

# -*- coding: utf-8 -*-

from nbx.tonic import Resource, fields
from nbx.models import FiscalData

class FiscalDataResource(Resource):

    class Meta:
        model = FiscalData

    class Schema:
        type = fields.String(dump_only=True)

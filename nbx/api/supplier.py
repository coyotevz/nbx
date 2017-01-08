from flask_potion import ModelResource, fields
from flask_potion.contrib.alchemy.fields import InlineModel

from nbx.models import Supplier, Address, Phone, BankAccount, FiscalData


class SupplierResource(ModelResource):

    class Meta:
        model = Supplier
        name = 'suppliers'
        exclude_fields = ['entity_type']
        include_id = True

    class Schema:
        rz = fields.String(attribute='_name_1')
        name = fields.String(attribute='_name_2')

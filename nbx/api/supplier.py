from flask_potion import ModelResource, fields
from flask_potion.routes import ItemRoute
from flask_potion.contrib.alchemy.fields import InlineModel

from nbx.models import Supplier

from .document import DocumentSchema
from .misc import AddressSchema, PhoneSchema, EmailSchema, TimestampMixin
from .bank import BankAccountSchema
from .fiscal import FiscalDataSchema


class SupplierResource(TimestampMixin, ModelResource):

    class Meta:
        model = Supplier
        name = 'suppliers'
        exclude_fields = ['entity_type']
        include_id = True

    class Schema:
        rz = fields.String(attribute='_name_1')
        name = fields.String(attribute='_name_2')
        address = fields.List(AddressSchema)
        email = fields.List(EmailSchema)
        phone = fields.List(PhoneSchema)
        bank_accounts = fields.List(BankAccountSchema)
        fiscal_data = FiscalDataSchema

    @ItemRoute.GET('/documents', rel="documents")
    def documents(self, supplier) -> fields.List(DocumentSchema):
        return supplier.documents

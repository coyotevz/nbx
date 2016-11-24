# -*- coding: utf-8 -*-

from sqlalchemy.ext.associationproxy import association_proxy

from nbx.models import db
from nbx.models.entity import Entity
from nbx.models.fiscal import FiscalData
#from nbx.models.product import ProductSupplierInfo

class Supplier(Entity):
    __tablename__ = 'supplier'
    __mapper_args__ = {'polymorphic_identity': 'supplier'}

    supplier_id = db.Column(db.Integer, db.ForeignKey('entity.id'),
                            primary_key=True)
    rz = Entity._name_1
    name = Entity._name_2

    fiscal_data_id = db.Column(db.Integer, db.ForeignKey('fiscal_data.id'))
    fiscal_data = db.relationship(FiscalData,
                                  backref=db.backref('entity', uselist=False))

    payment_term = db.Column(db.Integer) # in days
    leap_time = db.Column(db.Integer) # in days

    supplier_contacts = db.relationship('SupplierContact',
                                        cascade='all, delete-orphan',
                                        backref='supplier')
    contacts = association_proxy('supplier_contacts', 'contact')

    #: 'bank_accounts' attribute added by BankAccount.supplier relation
    #: 'orders' attribute added by PurchaseOrder.supplier relation

    #: Inherited from Entity
    #: - address (collection)
    #: - email (collection)
    #: - phone (collection)
    #: - extra field (collection)

#    documents = db.relationship('Document', backref="supplier", lazy='dynamic')
#    products = association_proxy('products_info', 'product')

    @property
    def full_name(self):
        n = " ({0})".format(self.name) if self.name else ''
        return "{0}{1}".format(self.rz, n)

    def add_contact(self, contact, role):
        self.supplier_contacts.append(SupplierContact(contact, role))

#    def add_product(self, product, **kwargs):
#        self.products_info.append(ProductSupplierInfo(product=product, **kwargs))


class SupplierContact(db.Model):
    __tablename__ = 'supplier_contact'
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'), primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.contact_id'), primary_key=True)
    role = db.Column(db.Unicode)

    contact = db.relationship('Contact', lazy='joined', backref='supplier_contacts')

    def __init__(self, contact, role):
        self.contact = contact
        self.role = role

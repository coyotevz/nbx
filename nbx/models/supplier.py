# -*- coding: utf-8 -*-

from sqlalchemy.ext.associationproxy import association_proxy

from nbx.models import db
from nbx.models.entity import Entity
from nbx.models.product import ProductSupplierInfo

class Supplier(Entity):
    __tablename__ = 'supplier'
    __mapper_args__ = {'polymorphic_identity': 'supplier'}

    supplier_id = db.Column(db.Integer, db.ForeignKey('entity.id'), primary_key=True)
    cuit = db.Column(db.Unicode(13), nullable=False)
    payment_term = db.Column(db.Integer)

    name = Entity._name_1
    fancy_name = Entity._name_2

    supplier_contacts = db.relationship('SupplierContact', cascade='all, delete-orphan', backref="supplier")
    contacts = association_proxy('supplier_contacts', 'contact')

    documents = db.relationship('Document', backref="supplier", lazy='dynamic')

    products = association_proxy('products_info', 'product')

    @property
    def fullname(self):
        retval = self.name
        retval += u" (%s)" % self.fancy_name if self.fancy_name else ''
        return retval

    def add_contact(self, contact, role):
        self.supplier_contacts.append(SupplierContact(contact, role))

    def add_product(self, product, **kwargs):
        self.products_info.append(ProductSupplierInfo(product=product, **kwargs))


class SupplierContact(db.Model):
    __tablename__ = 'supplier_contact'
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'), primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.contact_id'), primary_key=True)
    role = db.Column(db.Unicode)

    contact = db.relationship('Contact', lazy='joined', backref='supplier_contacts')

    def __init__(self, contact, role):
        self.contact = contact
        self.role = role

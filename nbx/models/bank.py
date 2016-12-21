# -*- coding: utf-8 -*-

from sqlalchemy.orm import validates

from nbx.models import db
from nbx.utils.validators import validate_cuit, validate_cbu

class Bank(db.Model):
    __tablename__ = 'bank'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True, nullable=False)
    bcra_code = db.Column(db.Unicode(8))
    cuit = db.Column(db.Unicode(11))
    # TODO: Add bank logo, to quickly identify

    @validates('cuit')
    def cuit_is_valid(self, key, cuit):
        if not validate_cuit(cuit):
            raise ValueError('CUIT Invalid')
        return cuit

class BankAccount(db.Model):
    __tablename__ = 'bank_account'

    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.Unicode)
    acc_type = db.Column(db.Unicode)

    number = db.Column(db.Unicode)
    owner = db.Column(db.Unicode)
    cbu = db.Column(db.Unicode)

    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)
    bank = db.relationship(Bank, backref='accounts')

    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    entity = db.relationship('Entity', backref='bank_accounts', lazy='joined')

    #supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'),
    #                        nullable=False)
    #supplier = db.relationship('Supplier', backref='bank_accounts',
    #                           lazy='joined')

    @validates('cbu')
    def cbu_is_valid(self, key, cbu):
        if not validate_cbu(cbu):
            raise ValueError('CBU invalid')
        return cbu

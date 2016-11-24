# -*- coding: utf-8 -*-

from nbx.models import db

class BankAccount(db.Model):
    __tablename__ = 'bank_account'

    id = db.Column(db.Integer, primary_key=True)
    bank = db.Column(db.Unicode(60), nullable=False)
    branch = db.Column(db.Unicode(60))
    acc_type = db.Column(db.Unicode(60), nullable=False)
    number = db.Column(db.Unicode(60), nullable=False)
    owner = db.Column(db.Unicode(60), nullable=False)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'),
                            nullable=False)
    supplier = db.relationship('Supplier', backref='bank_accounts',
                               lazy='joined')

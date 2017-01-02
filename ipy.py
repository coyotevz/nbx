# -*- coding: utf-8 -*-

from decimal import Decimal
from nbx.application import create_app
from nbx.models import (
    db, Address, Phone, Email, Entity, User, Contact, Supplier,
    SupplierContact, Document, Payment, DocumentPayment, BankAccount,
    PurchaseOrder, PurchaseOrderItem, Product, ProductSupplierInfo,
)

app = create_app()
ctx = app.test_request_context()
ctx.push()

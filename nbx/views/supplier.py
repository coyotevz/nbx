# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request, make_response
from flask import Blueprint
from werkzeug.urls import url_unquote

from nbx.models import db, Entity, Supplier, Product, ProductSupplierInfo, PurchaseOrder, Document, BankAccount
from nbx.forms import SupplierForm, ProductSupplierForm

supplier = Blueprint('supplier', __name__)

@supplier.route('/')
def index():
    suppliers = Supplier.query.order_by(Entity.id)
    return render_template('supplier/list.html', suppliers=suppliers)

@supplier.route('/<int:supplier_id>/')
def detail(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template('supplier/detail.html', supplier=supplier)

@supplier.route('/<int:supplier_id>/edit/', methods=['GET', 'POST'])
@supplier.route('/new/', methods=['GET', 'POST'])
def edit(supplier_id=None):
    supplier = Supplier()
    msg = u'El nuevo proveedor se creó satisfactoriamente.'
    if supplier_id:
        supplier = Supplier.query.get_or_404(supplier_id)
        msg = u'El proveedor se modificó satisfactoriamente.'
    if 'supplier_name' in request.cookies and not supplier.name:
        supplier.name = url_unquote(request.cookies.get('supplier_name'))
    form = SupplierForm(obj=supplier)
    if form.validate_on_submit():
        form.populate_obj(supplier)
        if not supplier.id:
            supplier.id = None
            db.session.add(supplier)
        db.session.commit()
        flash(msg)
        resp = make_response(redirect(url_for('.detail', supplier_id=supplier.id)))
    else:
        if not form.id.data:
            form.id.data = None
        resp = make_response(render_template('supplier/edit.html', form=form))
    resp.set_cookie('supplier_name', '')
    return resp

@supplier.route('/<int:supplier_id>/orders/')
def orders(supplier_id):
    orders = PurchaseOrder.query.filter_by(supplier_id=supplier_id)
    return render_template('supplier/orders.html', orders=orders)

@supplier.route('/<int:supplier_id>/documents/')
def documents(supplier_id):
    documents = Document.query.filter_by(supplier_id=supplier_id)
    return render_template('supplier/documents.html', documents=documents)

@supplier.route('/<int:supplier_id>/contacts/')
def contacts(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template('supplier/contacts.html', contacts=supplier.supplier_contacts, supplier=supplier)

@supplier.route('/<int:supplier_id>/contacts/new/')
def contact_new(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return '<#TODO>'

@supplier.route('/<int:supplier_id>/bank_acc/')
def bank_accounts(supplier_id):
    accounts = BankAccount.query.filter_by(supplier_id=supplier_id)
    return render_template('supplier/bank_accounts.html', accounts=accounts)

@supplier.route('/<int:supplier_id>/comments/')
def comments(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    return render_template('supplier/comments.html', comments=supplier.comments)

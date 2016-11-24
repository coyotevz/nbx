# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request, make_response
from flask import Blueprint
from werkzeug.urls import url_unquote

from nbx.models import db, Supplier, Product, ProductSupplierInfo
from nbx.forms import ProductForm, ProductSupplierForm, ProductSupplierInfoForm

product = Blueprint('product', __name__)

@product.route('/')
def index():
    products = Product.query.all()
    return render_template('product/list.html', products=products)

@product.route('/<int:product_id>/')
def detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product/detail.html', product=product)

@product.route('/<int:product_id>/edit/', methods=['GET', 'POST'])
@product.route('/new/', methods=['GET', 'POST'])
def edit(product_id=None):
    product = Product()
    msg = u'El nuevo producto se creó satisfactoriamente'
    if product_id:
        product = Product.query.get_or_404(product_id)
        msg = u'El producto se modificó satisfactoriamente'
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        if not product.id:
            product.id = None
            db.session.add(product)
        db.session.commit()
        flash(msg)
        return redirect(url_for('product.detail', product_id=product.id))
    if not form.id.data:
        form.id.data = None
    return render_template('product/edit.html', form=form)

@product.route('/supplier/<int:supplier_id>/')
def for_supplier(supplier_id):
    products_info = ProductSupplierInfo.query.filter_by(supplier_id=supplier_id)
    return render_template('product/for_supplier.html',
                           products_info=products_info,
                           supplier_id=supplier_id)

@product.route('/<int:product_id>/supplier/<int:supplier_id>/edit/', methods=['GET', 'POST'])
@product.route('/supplier/<int:supplier_id>/new/', methods=['GET', 'POST'])
def for_supplier_edit(supplier_id, product_id=None):
    supplier = Supplier.query.get_or_404(supplier_id)
    form = ProductSupplierInfoForm()

    if request.is_xhr:
        print("This request is XHR")

    if form.validate_on_submit():
        return redirect(url_for('.for_supplier', supplier_id=supplier.id))

    return render_template('product/for_supplier_edit.html', form=form, supplier=supplier)

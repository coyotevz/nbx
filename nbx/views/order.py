# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request, make_response
from flask import Blueprint

from nbx.models import db, PurchaseOrder

order = Blueprint('order', __name__)

@order.route('/')
def index():
    orders = PurchaseOrder.query.all()
    return render_template('order/list.html', orders=orders)

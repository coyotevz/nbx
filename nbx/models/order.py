# -*- coding: utf-8 -*-

from nbx.models import db
from nbx.models.misc import TimestampMixin


class PurchaseOrder(db.Model, TimestampMixin):
    __tablename__ = 'purchaseorder'

    (ORDER_CANCELLED,
     ORDER_QUOTING,
     ORDER_PENDING,
     ORDER_CONFIRMED,
     ORDER_CLOSED) = range(5)

    statuses = { ORDER_CANCELLED: u'Cancelled',
                 ORDER_QUOTING: u'Quoting',
                 ORDER_PENDING: u'Pending',
                 ORDER_CONFIRMED: u'Confirmed',
                 ORDER_CLOSED: u'Closed'
               }

    id = db.Column(db.Integer, primary_key=True)
    _status = db.Column("status", db.Integer, default=ORDER_QUOTING)
    open_date = db.Column(db.Date)
    expected_receival_date = db.Column(db.Date)
    receival_date = db.Column(db.Date)
    confirm_date = db.Column(db.Date)
    notes = db.Column(db.UnicodeText)

    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'), nullable=False)
    supplier = db.relationship('Supplier', backref="orders")

    @property
    def number(self):
        return self.id

    @property
    def status_str(self):
        status = self._status
        if not status in PurchaseOrder.statuses:
            raise Exception('Got an unexpected status value: %s' % status)
        return PurchaseOrder.statuses[status]

    @property
    def amount(self):
        return db.session.query(db.func.sum(PurchaseOrderItem.quantity*PurchaseOrderItem.cost)).filter(PurchaseOrderItem.order==self).scalar()


class PurchaseOrderItem(db.Model):
    __tablename__ = 'purchaseorder_item'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    quantity_received = db.Column(db.Integer, default=0)
    quantity_returned = db.Column(db.Integer)
    base_cost = db.Column(db.Numeric(10, 2))
    cost = db.Column(db.Numeric(10, 2))

    # sellable_id = db.Column(db.Integer, db.ForeignKey('sellable.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('purchaseorder.id'), nullable=False)
    order = db.relationship('PurchaseOrder', backref='items')

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref='order_items')

    @property
    def total(self):
        return self.quantity * self.cost

    @property
    def received_total(self):
        return self.quantity_received * self.cost

    @property
    def pending_quantity(self):
        return self.quantity - self.quantity_received

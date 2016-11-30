# -*- coding: utf-8 -*-

from decimal import Decimal
from nbx.models import db
from nbx.models.payment import DocumentPayment
from nbx.models.misc import TimestampMixin


class Document(db.Model, TimestampMixin):
    __tablename__ = 'document'

    TYPE_FACTURA_A = 'TYPE_FACTURA_A'
    TYPE_NOTA_CREDITO_A = 'TYPE_NOTA_CREDITO_A'
    TYPE_PRESUPUESTO = 'TYPE_PRESUPUESTO'

    _doc_type = {
        TYPE_FACTURA_A: 'Factura A',
        TYPE_NOTA_CREDITO_A: 'Nota de Crédito',
        TYPE_PRESUPUESTO: 'Presupuesto',
    }

    STATUS_PENDING = 'STATUS_PENDING'
    STATUS_EXPIRED = 'STATUS_EXPIRED'
    STATUS_PAID = 'STATUS_PAID'

    _doc_status = {
        STATUS_PENDING: 'Pendiente',
        STATUS_EXPIRED: 'Vencida',
        STATUS_PAID: 'Pagada',
    }

    id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.Enum(*_doc_type.keys(), name='doc_type'),
                         default=TYPE_FACTURA_A)
    point_sale = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    doc_status = db.Column(db.Enum(*_doc_status.keys(), name='doc_status'),
                       default=STATUS_PENDING)
    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    notes = db.Column(db.UnicodeText)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'),
                            nullable=False)

    #: document_payments added by DocumentPayment.document relationship

    def add_payment(self, payment, amount=None):
        if amount is None:
            amount = min([payment.amount, self.balance])
        self.document_payments.append(DocumentPayment(payment, amount))

    @property
    def type(self):
        return self._doc_type.get(self.doc_type)

    @property
    def status(self):
        return self._doc_status.get(self.doc_status)

    @property
    def full_desc(self):
        return u"%s %04d-%08d" % (self.type, self.point_sale, self.number)

    @property
    def cancelled_date(self):
        if self.state in (self.STATUS_PENDING, self.STATUS_EXPIRED):
            return None
        return Payment.query.join('document_payment')\
                            .filter(DocumentPayment.document==self)\
                            .order_by(Payment.date.desc())[0].date

    @property
    def balance(self):
        paid = db.session.query(db.func.sum(DocumentPayment.amount))\
                         .filter(DocumentPayment.document==self).scalar()\
                         or Decimal(0)
        return self.total - paid

    def __repr__(self):
        return "<Document '{}' of '{}' ({})>".format(self.full_desc,
                                                     self.supplier.rz,
                                                     self.status)

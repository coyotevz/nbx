# -*- coding: utf-8 -*-

from nbx.models import db
from nbx.models.payment import DocumentPayment
from nbx.models.misc import TimestampMixin


class Document(db.Model, TimestampMixin):
    __tablename__ = 'document'
    id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.Unicode(10), nullable=False)
    point_sale = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    _state = db.Column("state", db.Enum(u'EXPIRED', u'PENDING', u'PAID', name=u'State'), default=u'PENDING')
    issue_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    notes = db.Column(db.UnicodeText)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'), nullable=False)

    document_payments = db.relationship('DocumentPayment', cascade='all, delete-orphan', backref="document")

    def add_payment(self, payment, amount=None):
        if amount is None:
            amount = min([payment.amount, self.balance])
        self.document_payments.append(DocumentPayment(payment, amount))

    @property
    def fulldesc(self):
        return u"%s %04d-%08d" % (self.doc_type, self.point_sale, self.number)

    @property
    def cancelled_date(self):
        if self.state in (u'PENDING', u'EXPIRED'):
            return None
        return Payment.query.join('document_payment')\
                            .filter(DocumentPayment.document==self)\
                            .order_by(Payment.date.desc())[0].date

    @property
    def balance(self):
        paid = db.session.query(func.sum(DocumentPayment.amount))\
                         .filter(DocumentPayment.invoice==self).scalar() or Decimal(0)
        return self.total - paid

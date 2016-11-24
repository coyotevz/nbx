# -*- coding: utf-8 -*-

from datetime import datetime

from nbx.models import db
from nbx.models.misc import TimestampMixin

class Comment(db.Model, TimestampMixin):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.UnicodeText, nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                              nullable=False)
    created_by = db.relationship('User', backref="comments_created",
            lazy='joined', primaryjoin='User.user_id==Comment.modified_by_id')
    modified_by_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                               nullable=False)
    modified_by = db.relationship('User', backref='comments_modified',
            lazy='joined', primaryjoin='User.user_id==Comment.modified_by_id')
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'),
            nullable=False)
    supplier = db.relationship('Supplier', backref='comments', lazy='joined')

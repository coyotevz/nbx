# -*- coding: utf-8 -*-

from datetime import datetime

from nbx.models import db

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.UnicodeText, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                              nullable=False)
    created_by = db.relationship('User', backref="comments_created",
            lazy='joined', primaryjoin='User.user_id==Comment.modified_by_id')
    modified_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    modified_by_id = db.Column(db.Integer, db.ForeignKey('user.user_id'),
                               nullable=False)
    modified_by = db.relationship('User', backref='comments_modified',
            lazy='joined', primaryjoin='User.user_id==Comment.modified_by_id')
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id'),
            nullable=False)
    supplier = db.relationship('Supplier', backref='comments', lazy='joined')

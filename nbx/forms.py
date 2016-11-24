# -*- coding: utf-8 -*-

import decimal
import locale

from flask_wtf import Form
from wtforms import (BooleanField, DateField, DecimalField, FormField,
                     HiddenField, IntegerField, PasswordField, TextAreaField,
                     TextField, SubmitField, widgets)
from wtforms.ext.sqlalchemy.fields import (QuerySelectField,
                                           QuerySelectMultipleField)
from wtforms.validators import (Length, NumberRange, Optional, Required)

locale.setlocale(locale.LC_ALL, '')


class LocaleDecimalField(DecimalField):
    """Mimic DecimalField but support current locale number parsing."""

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = decimal.Decimal(str(locale.atof(valuelist[0])))
            except (decimal.InvalidOperation, ValueError):
                raise ValueError(self.gettext(u'Not a valid decimal value'))

    def _value(self):
        retval = super(LocaleDecimalField, self)._value()
        try:
            return retval.replace('.', locale.localeconf()['decimal_point'])
        except:
            return retval


class SupplierForm(Form):
    id = HiddenField()
    name = TextField(u'Razón Social', validators=[Required()])
    fancy_name = TextField(u'Nombre fantasía')
    cuit = TextField('CUIT')
    notes = TextAreaField('Notas')


class ProductForm(Form):
    id = HiddenField()
    code = TextField(u'Código')
    description = TextField(u'Descripción')
    brand = TextField(u'Marca')


class ProductSupplierInfoForm(Form):
    id = HiddenField()
    code = TextField(u'Código')
    description = TextField(u'Descripción')
    base_cost = LocaleDecimalField(u'Costo Base')


class ProductSupplierForm(Form):
    product = FormField(ProductForm)
    psi = FormField(ProductSupplierInfoForm)


class LoginForm(Form):
    next = HiddenField()

    remember = BooleanField("Remember me")
    username = TextField("Username", validators=[
                    Required(message="You must provide an email or username")])
    password = PasswordField("Password")
    submit = SubmitField("Login")

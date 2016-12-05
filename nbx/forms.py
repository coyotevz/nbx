# -*- coding: utf-8 -*-

import decimal
import locale

from flask_wtf import FlaskForm
from wtforms import (BooleanField, DateField, DecimalField, FormField,
                     HiddenField, IntegerField, PasswordField, TextAreaField,
                     TextField, SubmitField, SelectField, widgets)
from wtforms.ext.sqlalchemy.fields import (QuerySelectField,
                                           QuerySelectMultipleField)
from wtforms.validators import (Length, NumberRange, Optional, Required)

from nbx.models.fiscal import FiscalData

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


class FiscalDataForm(FlaskForm):
    id = HiddenField()
    cuit = TextField('CUIT')
    iibb = TextField('IIBB')
    fiscal_type = SelectField(
        'Insc. IVA',
        choices=[(k, v) for k, v in FiscalData._fiscal_types.items()]
    )


class SupplierForm(FlaskForm):
    id = HiddenField()
    rz = TextField('Razón Social', validators=[Required()])
    name = TextField('Nombre')
    notes = TextAreaField('Notas')

    payment_term = IntegerField('Plazo de pago')
    leap_time = IntegerField('Plazo de entrega')
    delivery_included = BooleanField('Incluye flete')

    fiscal_data = FormField(FiscalDataForm)


class ProductForm(FlaskForm):
    id = HiddenField()
    code = TextField(u'Código')
    description = TextField(u'Descripción')
    brand = TextField(u'Marca')


class ProductSupplierInfoForm(FlaskForm):
    id = HiddenField()
    code = TextField(u'Código')
    description = TextField(u'Descripción')
    base_cost = LocaleDecimalField(u'Costo Base')


class ProductSupplierForm(FlaskForm):
    product = FormField(ProductForm)
    psi = FormField(ProductSupplierInfoForm)


class LoginForm(FlaskForm):
    next = HiddenField()

    remember = BooleanField("Remember me")
    username = TextField("Username", validators=[
                    Required(message="You must provide an email or username")])
    password = PasswordField("Password")
    submit = SubmitField("Login")

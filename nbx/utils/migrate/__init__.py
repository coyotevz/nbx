# -*- coding: utf-8 -*-

"""
    nbx.utils.migrate
    ~~~~~~~~~~~~~~~~~

    Migration script for old database, this file is part of nbx project.
"""

import click
from sqlalchemy import func

# new app
from nbx.application import create_app
from nbx.models import Supplier, FiscalData, Contact, Phone, Email, db

# old app
from .proveedores import (Comentario, CuentaBanco, Factura, Pedido, PedidoSub,
                          Proveedor, configure_session)

app = create_app()

def check_year(date):
    if date.year < 2000:
        return date.replace(year=(2000+date.year))
    return date

def _cuit(cuit):
    return cuit.replace('-','')

# NOTE:
# ~~~~
# PedidoSub --> PurchaseOrder
# Pedido    --> PurchaseOrderItem

def migrate_suppliers(s):
    tot = s.query(func.count(Proveedor.id)).scalar()
    with click.progressbar(s.query(Proveedor), length=tot,
                           label='* Migrando tabla proveedores') as proveedores:
        for p in proveedores:
            notes = s.query(Comentario).filter(Comentario.id_coment_proveedor==p.id).value('comentario')

            supplier = Supplier(rz=p.nombre,
                                web=p.web,
                                payment_term=p.plazo,
                                delivery_included=p.flete.startswith('A Cargo del Proveedor'),
                                notes = notes if notes else None)
            if p.cuit:
                fiscal = FiscalData(cuit=_cuit(p.cuit), iibb=p.ingresosBrutos,
                        fiscal_type=FiscalData.FISCAL_RESPONSABLE_INSCRIPTO)
                supplier.fiscal_data = fiscal
            if p.email:
                email = Email(email_type='Principal',
                              email=p.email)
                supplier.email.append(email)
            if p.fax:
                fax = Phone(phone_type='FAX',
                            number=p.fax)
                supplier.phone.append(fax)
            if p.direccion:
                address = Address(street=p.direccion,
                                  province='<unknown>',
                                  zip_code=p.codigo_postal)

            if p.nombre_contacto:
                fn, ln = (p.nombre_contacto.rsplit(' ', 1) + [None])[:2]
                contact = Contact(first_name=fn, last_name=ln)
                if p.telefono_contacto:
                    phone = Phone(phone_type='Principal',
                                  number=p.telefono_contacto)
                    contact.phone.append(phone)
                if p.email_contacto:
                    email = Email(email_type='Principal',
                                  email=p.email_contacto)
                    contact.email.append(email)
                supplier.add_contact(contact, 'Importado')

            db.session.add(supplier)
        db.session.commit()

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
from nbx.models import Supplier, db

# old app
from .proveedores import (Comentario, CuentaBanco, Factura, Pedido, PedidoSub,
                          Proveedor, configure_session)

app = create_app()

def check_year(date):
    if date.year < 2000:
        return date.replace(year=(2000+date.year))
    return date

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
            db.session.add(supplier)
        db.session.commit()

# -*- coding: utf-8 -*-

"""
    nbx.utils.migrate
    ~~~~~~~~~~~~~~~~~

    Migration script for old database, this file is part of nbx project.
"""

from datetime import date
from decimal import Decimal

import click
# new app
from nbx.application import create_app
from nbx.models import (Address, Contact, Document, Email, FiscalData, Phone,
                        Supplier, PurchaseOrder, PurchaseOrderItem, db)
from sqlalchemy import func

# old app
from .proveedores import (Comentario, CuentaBanco, Factura, Pedido, PedidoSub,
                          Proveedor, configure_session)

app = create_app()
today = date.today()

def check_year(date):
    if date.year < 2000:
        return date.replace(year=(2000+date.year))
    return date

def _cuit(cuit):
    return cuit.replace('-','')

doc_type_map = {
    'Factura A': Document.TYPE_FACTURA_A,
    'Nota de Crédito': Document.TYPE_NOTA_CREDITO_A,
    'Presupuesto': Document.TYPE_PRESUPUESTO,
}

po_status_map = {
    'Pedido sin Pendientes': PurchaseOrder.STATUS_CLOSED,
    'Articulos Pendientes': PurchaseOrder.STATUS_PARTIAL,
    'Pendiente de Entrega': PurchaseOrder.STATUS_CONFIRMED,
    'No Realizado': PurchaseOrder.STATUS_DRAFT,
}

po_method_map = {
    'Fax': PurchaseOrder.METHOD_FAX,
    'Personalmente': PurchaseOrder.METHOD_PERSONALLY,
    'e-mail': PurchaseOrder.METHOD_EMAIL,
}

# NOTE:
# ~~~~
# PedidoSub --> PurchaseOrder
# Pedido    --> PurchaseOrderItem

def migrate_document(s, f, supplier):
    doc_status = Document.STATUS_PENDING if not f.estado_fiscal else Document.STATUS_PAID
    if not f.estado_fiscal and f.fecha_de_vencimiento < today:
        doc_status = Document.STATUS_EXPIRED
    doc = Document(issue_date=check_year(f.fecha_de_emision),
                   expiration_date=check_year(f.fecha_de_vencimiento),
                   doc_type=doc_type_map[f.tipo_Factura],
                   point_sale=1, # no information about this
                   number=f.numero_factura,
                   total=Decimal(f.monto),
                   notes=f.descripcion if f.hay_coment == 'Si' else None,
                   doc_status=doc_status)
    supplier.documents.append(doc)

def migrate_order(s, p, supplier):
    po = PurchaseOrder(number=p.numero_pedido,
                       po_status=po_status_map[p.estado_de_pedido],
                       notes=p.comentario,
                       open_date=check_year(p.fecha_de_pedido),
                       po_method=po_method_map[p.medio_de_pedido],
                       supplier=supplier)

    items = s.query(Pedido).filter(Pedido.id_proveedor==p.id_proveedor)\
                           .filter(Pedido.numero_pedido==p.numero_pedido)

    for item in items:
        poi = PurchaseOrderItem(sku=item.codigo,
                                description=item.descripcion,
                                quantity=item.cantidad,
                                quantity_received=item.cantidad_recibida,
                                order=po)
    db.session.add(po)


def migrate_bank_account(s, cuenta, supplier):
    pass

def migrate_suppliers(s):
    tot = s.query(func.count(Proveedor.id)).scalar()
    with click.progressbar(s.query(Proveedor), length=tot,
                           label='* Migrate proveedores') as proveedores:
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
                supplier.address.append(address)

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
            for factura in s.query(Factura).filter(Factura.id_proveedor==p.id):
                migrate_document(s, factura, supplier)
            for pedido in s.query(PedidoSub).filter(PedidoSub.id_proveedor==p.id):
                migrate_order(s, pedido, supplier)
            for cuenta_banco in s.query(CuentaBanco).filter(CuentaBanco.id_proveedor==p.id):
                migrate_bank_account(s, cuenta_banco, supplier)
        db.session.commit()

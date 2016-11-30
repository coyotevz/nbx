# -*- coding: utf-8 -*-

from nbx.models import db


class FiscalData(db.Model):
    __tablename__ = 'fiscal_data'

    FISCAL_CONSUMIDOR_FINAL = 'CONSUMIDOR FINAL'
    FISCAL_RESPONSABLE_INSCRIPTO = 'RESPONSABLE INSCRIPTO'
    FISCAL_EXCENTO = 'EXCENTO'
    FISCAL_MONOTRIBUTO = 'MONOTRIBUTO'

    _fiscal_types = {
        FISCAL_CONSUMIDOR_FINAL: 'Consumidor Final',
        FISCAL_RESPONSABLE_INSCRIPTO: 'Responsable Inscripto',
        FISCAL_EXCENTO: 'Excento',
        FISCAL_MONOTRIBUTO: 'Monotributo',
    }

    id = db.Column(db.Integer, primary_key=True)
    cuit = db.Column(db.Unicode(13))
    fiscal_type = db.Column(db.Enum(*_fiscal_types, name='fiscal_type'),
                            default=FISCAL_CONSUMIDOR_FINAL)
    iibb = db.Column(db.Unicode, nullable=True)

    @property
    def needs_cuit(self):
        return self.fiscal_type not in (self.FISCAL_CONSUMIDOR_FINAL,)

    @property
    def type(self):
        return self._fiscal_type.get(self.fiscal_type)

    def __repr__(self):
        return "<FiscalData '{} {}' of '{}'>".format(
            self.fiscal_type,
            self.cuit,
            self.entity.full_name,
        )

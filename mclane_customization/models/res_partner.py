# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    license_number = fields.Char('License Number')
    license_file = fields.Binary('License File')
    expiration_date = fields.Date('Expiration Date')

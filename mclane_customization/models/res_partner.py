# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    license_number_cig = fields.Char('License Number')
    license_file_cig = fields.Binary('License File')
    license_filename_cig = fields.Char("License Filename")
    start_date_cig = fields.Date('Start Date')
    expiration_date_cig = fields.Date('Expriration Date')

    license_number_sale = fields.Char('License Number')
    license_file_sale = fields.Binary('License File')
    license_filename_sale = fields.Char("License Filename")
    start_date_sale = fields.Date('Start Date')
    expiration_date_sale = fields.Date('Expriration Date')

    license_number_tc = fields.Char('License Number')
    license_file_tc = fields.Binary('License File')
    license_filename_tc = fields.Char("License Filename")
    start_date_tc = fields.Date('Start Date')
    expiration_date_tc = fields.Date('Expriration Date')

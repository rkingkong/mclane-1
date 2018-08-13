from odoo import fields,api,models

class picking_hazardous(models.Model):
    _name = 'picking.hazardous'

    name = fields.Char(string='File Description')
    file = fields.Binary(string='File')
    file_attachment = fields.Many2one('ir.attachment')
    product_id = fields.Many2one(comodel_name='product.template',string='Product')

class product_template_hazardous(models.Model):
    _inherit = 'product.template'

    hazardous_files = fields.One2many(comodel_name='picking.hazardous',string='Hazardous Documents',inverse_name='product_id')


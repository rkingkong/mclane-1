from odoo import fields,api,models

class product_product(models.Model):
    _inherit = 'product.product'

    msrp_cost = fields.Float('MSRP', required=True, default=0.0)
    margin_msrp = fields.Float('Margin',default=0.0,compute='_calc_margin')


    @api.multi
    def _calc_margin(self):
        for prod_ob in self:
            prod_ob.margin_msrp = prod_ob.msrp_cost - prod_ob.list_price



class product_template(models.Model):
    _inherit = 'product.template'

    msrp_cost = fields.Float('MSRP', required=True, default=0.0)
    margin_msrp = fields.Float('Margin',default=0.0,compute='_calc_margin')


    @api.multi
    def _calc_margin(self):
        for prod_ob in self:
            prod_ob.margin_msrp = prod_ob.msrp_cost - prod_ob.list_price


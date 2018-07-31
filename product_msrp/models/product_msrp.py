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

class res_partner(models.Model):
    _inherit = 'res.partner'

    # Cron Job Function
    @api.multi
    def check_expired_license(self):
        today_date = fields.Date.context_today(self)
        partners = self.search(['|','|',('expiration_date_cig','>=',today_date),
                    ('expiration_date_sale','>=',today_date),
                    ('expiration_date_tc','>=',today_date)])
        print(today_date)
        if partners:
           for res in partners:
               if res.expiration_date_cig >= today_date:
                   res.csr_review_cig = False
               if res.expiration_date_sale >= today_date:
                   res.csr_review_sale = False
               if res.expiration_date_tc >= today_date:
                   res.csr_review_tc = False


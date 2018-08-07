from odoo import fields,api,models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError

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

    licenses_ids = fields.One2many(comodel_name='res.partner.flexible.cat',inverse_name='partner_id',string='Licenses')

    # Cron Job Function
    @api.multi
    def check_expired_license(self):
        today_date = fields.Date.context_today(self)
        partners = self.search(['|','|',('expiration_date_cig','<=',today_date),
                    ('expiration_date_sale','<=',today_date),
                    ('expiration_date_tc','<=',today_date)])
        if partners:
           for res in partners:
               if res.expiration_date_cig and res.expiration_date_cig <= today_date:
                   res.csr_review_cig = False
               if res.expiration_date_sale and res.expiration_date_sale <= today_date:
                   res.csr_review_sale = False
               if res.expiration_date_tc and res.expiration_date_tc <= today_date:
                   res.csr_review_tc = False



class res_partner_flexible_cat(models.Model):
    _name = 'res.partner.flexible.cat'

    product_category = fields.Many2one(comodel_name='product.public.category',string='Product Category')
    license_number = fields.Char('License Number',required=True)
    license_file = fields.Binary('License File')
    license_filename = fields.Char("License Filename")
    license_file_attachment = fields.Many2one('ir.attachment')
    start_date = fields.Date('Start Date')
    expiration_date = fields.Date('Expiration Date')
    no_expiration_date = fields.Boolean('No Expiration Date')
    csr_review= fields.Boolean('CSR Reviewed')
    partner_id = fields.Many2one(comodel_name='res.partner',string='Customer')

    @api.constrains('start_date', 'expiration_date')
    def check_dates(self):
        if self.no_expiration_date == False and self.start_date >= self.expiration_date :
            raise ValidationError(_('Error!  start-date must be lower then leave expiration-date.'))


    @api.onchange('no_expiration_date','expiration_date','start_date')
    def onchange_no_expiration_date(self):
        if self.no_expiration_date == True:
            self.expiration_date = False

        if self.expiration_date and self.start_date:
            if self.start_date >= self.expiration_date and self.no_expiration_date == False:
                raise ValidationError(_('Error!  start-date must be lower then leave expiration-date.'))


    # Cron Job Function For Licenses Ids
    @api.multi
    def check_expired_license_ids(self):
        today_date = fields.Date.context_today(self)
        expired_licenses = self.search([('expiration_date', '<=', today_date)])
        print(expired_licenses)
        if expired_licenses:
            for res in expired_licenses:
                if res.expiration_date and res.expiration_date <= today_date:
                    res.csr_review = False
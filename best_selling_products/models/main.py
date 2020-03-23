from odoo import models, api, fields
from datetime import datetime

from heapq import nlargest
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    publish_date = fields.Datetime('Publish date')

    @api.model
    def create(self, vals):
        if vals.get('website_published',False) or self.website_published:
            vals['publish_date'] = fields.datetime.now()

        return super(ProductTemplate,self).create(vals)

class ProductPublicCategory(models.Model):

    _inherit = "product.public.category"

    product_ids = fields.Many2many('product.template')
    best_selling_product_ids = fields.Many2many('product.template', 'product_sale_count_rel', 'sales_count',string="Best Selling Products")
    latest_product_ids = fields.Many2many('product.template', 'product_publish_date_rel', 'publish_date',string="Latest Products")

    @api.model
    def Merge(self, list1, list2):
        new_list = list1 + list2
        new_list.sort()
        return new_list

    @api.model
    def update_best_selling_products(self):
        total_best_selling_products = int(self.env['res.config.settings'].get_values()['total_best_selling_products']) or int("3")
        total_latest_products = int(self.env['res.config.settings'].get_values()['total_latest_products']) or int("3")

        _logger.info("total_latest_products%r",total_latest_products)

        for website_id in self.env['website'].search([]):
            website_id.write({
                'best_selling_product_ids':[(6,0,self.env['product.template'].search([('website_published','=',True)], order='sales_count desc', limit = total_best_selling_products).mapped('id'))],
                'latest_product_ids':[(6,0,self.env['product.template'].search([('website_published','=',True)], order='publish_date desc', limit = total_latest_products).mapped('id'))],
            })

        for rec in self.search([]):
            temp_best_selling_data = dict()
            temp_latest_selling_data = dict()
            for product_id in rec.product_ids:
                if product_id.website_published == True and product_id.publish_date:
                    temp_best_selling_data[product_id.id] = product_id.sales_count
                    temp_latest_selling_data[product_id.id] = datetime.strptime(product_id.publish_date,'%Y-%m-%d %H:%M:%S')

            rec.best_selling_product_ids = [(6,0,nlargest(total_best_selling_products, temp_best_selling_data, key = temp_best_selling_data.get))]
            rec.latest_product_ids = [(6,0,nlargest(total_latest_products, temp_latest_selling_data, key = temp_latest_selling_data.get))]

            if rec.parent_id:
                rec.parent_id.best_selling_product_ids = [(6,0,self.Merge(
                        rec.best_selling_product_ids.mapped('id'),
                        rec.parent_id.best_selling_product_ids.mapped('id')
                        )[-total_best_selling_products:]
                    )]
                rec.parent_id.latest_product_ids = [(6,0,self.Merge(rec.latest_product_ids.mapped('id'),
                        rec.parent_id.latest_product_ids.mapped('id')
                        )[-total_latest_products:]
                    )]

class Website(models.Model):
    _inherit = 'website'

    best_selling_product_ids = fields.Many2many('product.template', 'sales_count_rel','product_id','best_selling_id',string="Best Selling Products")
    latest_product_ids = fields.Many2many('product.template', 'publish_date_rel','product_id','latest_product_id',string="Latest Products")

    # cat_best_selling_product_ids = fields.Many2many('product.public.category', 'best_selling_product_ids_rel', 'category_id', 'best_selling_id', string="Best Selling Product By categories")
    # cat_latest_product_ids = fields.Many2many('product.public.category', 'latest_product_ids_rel', 'category_id', 'latest_product_id', string="Latest Products By Category")

    total_best_selling_products = fields.Char('Total Best Selling Products')
    total_latest_products = fields.Char('Total Latest Selling Products')

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    best_selling_product_ids = fields.Many2many('product.template',string="Best Selling Products", related="website_id.best_selling_product_ids")
    latest_product_ids = fields.Many2many('product.template',string="Latest Products", related="website_id.latest_product_ids")

    # cat_best_selling_product_ids = fields.Many2many('product.public.category', related="website_id.cat_best_selling_product_ids",string="Best Selling Product By categories")
    # cat_latest_product_ids = fields.Many2many('product.public.category', 'latest_product_ids_rel',related="website_id.cat_latest_product_ids", string="Latest Products By Category")

    # cat_best_selling_product_ids = fields.Many2many()
    # cat_latest_product_ids = fields.Many2many()

    total_best_selling_products = fields.Char('Total Best Selling Products', related="website_id.total_best_selling_products", default='3')
    total_latest_products = fields.Char('Total Best Selling Products', related="website_id.total_latest_products", default='3')


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            total_best_selling_products = self.env['ir.config_parameter'].sudo().get_param('website.total_best_selling_products', default='3'),
            total_latest_products = self.env['ir.config_parameter'].sudo().get_param('website.total_latest_products', default='3'),
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('website.total_best_selling_products',self.total_best_selling_products)
        self.env['ir.config_parameter'].sudo().set_param('website.total_latest_products',self.total_latest_products)

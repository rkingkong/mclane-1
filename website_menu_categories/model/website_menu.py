# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.http import request
import re

class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'
    menu_id = fields.Many2one('website.menu', string="Website Menu")
    website_id = fields.Many2one('website', string="Website")

    def create_menu(self):
        for category in self:
            category_name=re.sub("[!@#$%^&*()[]{};:,./<>?\|`~=_+\/]", "-", category.name)
            url='/shop/category/%s-%s' % (category_name.replace(" ","-"),category.id)
            category.menu_id=self.env['website.menu'].search([('url','=',url)], limit=1).id or False           
            if category.parent_id and not category.parent_id.menu_id:
                category.parent_id.create_menu()
            if not category.menu_id:
                data={'to_delete': False,
                      'data':[{
                             'url': url,
                             'name': category.name,
                             'sequence':1,
                             'id': 'new-3',
                             'parent_id':self.env['website.menu'].search([('url','=','/shop')], limit = 1).id or False,
                             }],
                     }
                self.env['website.menu'].save(category.website_id, data)
                category.menu_id=self.env['website.menu'].search([('url','=',url)], limit=1).id or False
        return

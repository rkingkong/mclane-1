# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
##########################################################################
from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        result = super(WebsiteSale, self).product(product=product, category=category, search=search, **kwargs)
        if request.session.uid:
            self.add_viewed_product(product)
        result.qcontext['viewed_product'] = self.get_viewed_products()
        return result
    
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>'
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        result = super(WebsiteSale, self).shop(page=page, category=category, search=search, ppg=ppg, **post)
        result.qcontext['viewed_product'] = self.get_viewed_products()
        return result

    def get_viewed_products(self):
        user_obj, viewed_product = request.env['res.users'], []
        default_context = dict(request.env.context)
        pricelist = request.website.get_current_pricelist()
        if not default_context.get('pricelist'):
            default_context['pricelist'] = pricelist.id

        user_viewed_products = user_obj.with_context(default_context).browse(request.uid).recently_viewed_products

        for view in user_viewed_products:
            viewed_product.append(view.product_id)
        return viewed_product

    def add_viewed_product(self, product):
        viewed_obj = request.env['wk.recently.view']
        user_obj = request.env['res.users']
        viewed_id = viewed_obj.search([('ref_id', '=', request.uid), ('product_id', '=', product.id)])
        if viewed_id:
            viewed_obj.update_viewed(viewed_id[0].id)
        else:
            record_id = viewed_obj.create_viewed(product.id)

        number = request.website.get_max_and_allow_product_qty(1)
        user_viewed_products = user_obj.browse(request.uid).recently_viewed_products
        if user_viewed_products:
            if len(user_viewed_products) > number:
                temp = user_viewed_products[number:]
                for rec in temp:
                    rec.unlink()

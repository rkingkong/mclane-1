# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale

PPG = 20  # Products Per Page
PPR = 4   # Products Per Row

class WebsiteSale(WebsiteSale):
    @http.route(["/buy_again",'''/buy_again/page/<int:page>''',
    '''/buy_again/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',
    '''/buy_again/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>'''], type="http", website=True, auth="public")
    def buy_again(self, page=0, category=None, search='', ppg=False, **post):
        res  = self.shop(page, category, search, ppg)
        orders = request.env.user.partner_id.sale_order_ids.filtered(lambda l: l.state in ('sale', 'done'))
        cur_user = request.env.user
        buy_again_config = request.env['buy.again.config'].search([('set_active', '=', True),('website_id','=',request.website.id)], limit=1)
        purchased_products = []
        for ord in orders:
            for p in ord.order_line:
                if not len(buy_again_config) or not buy_again_config.from_date:
                    purchased_products.append(p.product_id.product_tmpl_id.id)
                else:
                    if buy_again_config.from_date:
                        if ord.date_order >= buy_again_config.from_date:
                            purchased_products.append(p.product_id.product_tmpl_id.id)

        purchased_products = list(set(purchased_products))
        if len(buy_again_config):
            if buy_again_config.product_limit:
                purchased_products = purchased_products[:buy_again_config.product_limit]

        if category:
            url = "/buy_again/category/%s" % slug(category)

        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = PPG
            post["ppg"] = ppg
        else:
            ppg = PPG
        url = "/buy_again"

        Product = request.env['product.template'].with_context(bin_size=True)
        pager = request.website.pager(url=url, total=len(purchased_products), page=page, step=ppg, scope=5, url_args=post)
        products = Product.search([('id','in', purchased_products)], limit=ppg, offset=pager['offset'], order=self._get_search_order(post))

        res.qcontext['pager'] = pager
        res.qcontext['products'] = products
        res.qcontext['bins'] = TableCompute().process(products, ppg)
        res.qcontext['keep'] = QueryURL('/buy_again')
        return res

from odoo import http,fields
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website.controllers.main import Website

import logging
_logger = logging.getLogger(__name__)

class BestSelling(http.Controller):

    non_url_safe = ['"', '#', '$', '%', '&', '+',
                    ',', '/', ':', ';', '=', '?',
                    '@', '[', '\\', ']', '^', '`',
                    '{', '|', '}', '~', "'"]

    def slugify(self, text):
        non_safe = [c for c in text if c in self.non_url_safe]
        text = text.lower()
        if non_safe:
            for c in non_safe:
                text = text.replace(c, '')
        text = u'-'.join(text.split())
        return text

    def _set_values(self,product_ids, category):
        values = []
        for product_id in product_ids:
            url = self.slugify((product_id.default_code or '') +' '+product_id.name+' '+str(product_id.id))+('?category='+str(category.id) if category else '')
            attrs = {
                'in_wish': True if product_id.product_variant_ids[0] in request.env['product.wishlist'].current().mapped('product_id') else False,
                'product_id': product_id.id,
                'product_varient_id': product_id.product_variant_ids[0].id,
                'name': product_id.name,
                'image': product_id.image,
                'price': product_id.list_price,
                'curr_symbol': product_id.currency_id.symbol,
                'url': '/shop/product/'+url,
            }
            values.append(attrs)
        return values

    def _get_product_ids(self,category,type=None):
        return getattr(category, type) if category else getattr(request.website, type)

    def _get_best_selling_products(self,category):
        return self._set_values(self._get_product_ids(category,type='best_selling_product_ids'), category)

    def _get_latest_products(self,category):
        return self._set_values(self._get_product_ids(category,type='latest_product_ids'), category)


    @http.route([
        '/get_wk_products/shop',
        '/get_wk_products/shop/page/<int:page>',
        '/get_wk_products/shop/category/<model("product.public.category"):category>',
        '/get_wk_products/shop/category/<model("product.public.category"):category>/page/<int:page>'
        ], type="json", auth="public", website=True)
    def get_wk_products(self, category=False,page=1,**kw):
        return {
            'best_selling_products':self._get_best_selling_products(category),
            'latest_products': self._get_latest_products(category),
        }



class Website(Website):

    @http.route()
    def publish(self, id, object):
        res = super(Website,self).publish(id, object)
        if object == 'product.template' and res:
            Model = request.env[object]
            record = Model.browse(int(id))
            record.publish_date = fields.Datetime.now()
        return res

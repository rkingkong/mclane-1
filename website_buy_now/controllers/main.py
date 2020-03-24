# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################

import logging
import json
from ast import literal_eval
from math import isclose

from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import route, request
_log = logging.getLogger(__name__)

class WebBuyNow(WebsiteSale):

    def get_user_cart_data(self):
        try:
            return literal_eval(request.env['res.users'].browse(request._uid).partner_id.save_user_cart_data)
        except Exception as e:
            return {}

    def update_user_cart_data(self, data):
        if data:
            res_partner = request.env['res.users'].browse(request._uid).partner_id
            res_partner.write({'save_user_cart_data': data})



    def check_cart_in_session(self):
        cart = {}
        if request.website.is_public_user():
            cart_data = request.session.get('product_for_later')
            request.session['product_for_later'] = None
        else:
            res_partner = request.env['res.users'].browse(request._uid).partner_id
            try:
                cart_data = literal_eval(res_partner.save_user_cart_data)
            except Exception as e:
                cart_data = {}
            finally:
                res_partner.write({'save_user_cart_data' : ''})
        if cart_data:
            sale_order = request.website.sale_get_order(force_create=1)
            for line in cart_data:
                sale_order._cart_update(product_id = int(line),line_id = None,add_qty = int(cart_data[line]))
            return sale_order
        return False

    @route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update(self, product_id=0, add_qty=1, set_qty=0, **kw):
        if int(product_id):
            sale_order = request.website.sale_get_order(force_create=1)
            if sale_order.state in ['sent']:
                request.session['sale_order_id'] = None
            if kw.get('buy_now'):
                sale_order = request.website.sale_get_order(force_create=1)
                user_type = request.website.is_public_user()
                product_for_later = request.session.get('product_for_later') if user_type else self.get_user_cart_data()
                if not product_for_later:
                    product_for_later = {}
                    for lines in sale_order.order_line:
                        if product_for_later.get(lines.id):
                            product_for_later.update({lines.product_id.id : lines.product_uom_qty+product_for_later.get(lines.id)})
                        else:
                            product_for_later.update({lines.product_id.id : lines.product_uom_qty})
                        lines.unlink()
                else:
                    prev_product_id = sale_order.order_line[0].product_id.id
                    if product_for_later.get(prev_product_id):
                        product_for_later.update({prev_product_id : product_for_later.get(prev_product_id)+sale_order.order_line[0].product_uom_qty})
                    else:
                        product_for_later.update({prev_product_id : sale_order.order_line[0].product_uom_qty})
                    sale_order.order_line[0].unlink()
                if user_type:
                    request.session['product_for_later'] = product_for_later
                if not user_type:
                    self.update_user_cart_data(json.dumps(product_for_later))
                super(WebBuyNow, self).cart_update(product_id=product_id, add_qty = add_qty, set_qty=set_qty, **kw)
                return request.redirect('/shop/checkout')
            return super(WebBuyNow, self).cart_update(product_id=product_id, add_qty = add_qty, set_qty=set_qty, **kw)
        return request.redirect("/shop")


    @route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, access_token=None, revive='', **post):
        if post.get('type') != 'popover':
            self.check_cart_in_session()
        return super(WebBuyNow, self).cart(access_token=access_token, revive=revive, **post)

    @route(['/shop/confirmation'], type='http', auth="public", website=True)
    def payment_confirmation(self, **post):
        data = super(WebBuyNow, self).payment_confirmation(**post)
        self.check_cart_in_session()
        return data

    @route(['/buy_now/get-totalquantity'], type = "http", auth = "public", website = True)
    def get_total_quantity_in_cart(self, **kw):
        sale_order = self.check_cart_in_session()
        total_quantity = 0
        if not sale_order:
            sale_order = request.website.sale_get_order()
        if sale_order:
            total_quantity = sale_order.cart_quantity
        return json.dumps({"total_quantity":total_quantity})

    @route(['/buy_now/check/product/integrity'], type="json", auth="public", website=True)
    def check_product_integrity(self, product_id=0, qty=0, products=0, **kw):
        redirect = True
        sale_order = request.website.sale_get_order()
        try:
            if (product_id and len(sale_order.website_order_line.ids)==1 and qty):
                line = sale_order.website_order_line
                if line.product_id.id == int(product_id) and qty == line.product_uom_qty:
                    redirect = False
        except Exception as e:
            redirect = True
            _log.error("Transeaction failed due to integrity of price in buy now option")
        return {"redirect":redirect}

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
from odoo import api, models, fields, tools, _
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = 'website'

    @api.model
    def get_max_and_allow_product_qty(self, value=0):
        if value == 1:
            number = self.env['ir.default'].sudo().get('res.config.settings', 'wk_maximum_product')
        if value == 2:
            number = self.env['ir.default'].sudo().get('res.config.settings', 'wk_show_product')
        if number:
        	return number
        return 0

    @api.model
    def viewed_product(self):
        return self.get_viewed_products()

    @api.model
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

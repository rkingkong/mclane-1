# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE URL <https://store.webkul.com/license.html/> for full copyright and licensing details.
#################################################################################
from odoo import models, fields, api
from odoo.http import request
import logging
_log = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    save_user_cart_data = fields.Text('Save Cart Data')


class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def sale_get_order(self, force_create=False, code=None, update_pricelist=False, force_pricelist=False):
        if request.session.get('sale_order_id') and not request.website.is_public_user():
            sale_order_id = self.env['res.users'].browse(self._uid).partner_id.last_website_so_id.id
            if request.session.get('sale_order_id') != sale_order_id:
                request.session['sale_order_id'] = sale_order_id
        return super(Website, self).sale_get_order(force_create=force_create, code=code, update_pricelist=update_pricelist, force_pricelist=force_pricelist)

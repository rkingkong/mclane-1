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

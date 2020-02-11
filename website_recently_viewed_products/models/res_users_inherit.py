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


class ResUsers(models.Model):
    _inherit = 'res.users'

    recently_viewed_products = fields.One2many('wk.recently.view', 'ref_id', string='Recently Viewed Product')


class WkRecentlyView(models.Model):
    _name = 'wk.recently.view'
    _order = 'view_date desc'

    ref_id = fields.Many2one('res.users', string="user")
    product_id = fields.Many2one('product.template', string="Product")
    view_date = fields.Datetime(string="View Date")

    @api.model
    def create_viewed(self, product):
        if product:
            record_id = self.create({'ref_id': self._uid, 'product_id': product, 'view_date': fields.datetime.now()})
            return record_id
        return False

    @api.model
    def update_viewed(self, record_id):
        if record_id:
            self.browse(record_id).write({'view_date': fields.datetime.now()})

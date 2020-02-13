# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class WebkulWebsiteAddons(models.TransientModel):
    _inherit = 'webkul.website.addons'

    module_website_buy_again = fields.Boolean(string="Website Buy Again Products")

class BuyAgainConfig(models.Model):
    _name = "buy.again.config"
    _description = "Buy again configuration"

    name = fields.Char("Title", required=True)
    website_id = fields.Many2one('website', string='Website', required=True)
    from_date = fields.Datetime("From date")
    product_limit = fields.Integer("Product Limit")
    menu_buy_again = fields.Char(default="Buy Again", translate=True)
    set_active = fields.Boolean(default=False, track_visibility='onchange')

    @api.multi
    def toggle_set_active(self):
        if self.set_active:
            self.set_active = False
        else:
            rec = self.search([('set_active','=',True),('website_id','=',self.website_id.id)], limit=1)
            if len(rec):
                raise UserError(_('Some setting is already in active state. Please make that inactive first.'))
            else:
                self.set_active = True

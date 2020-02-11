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
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    wk_maximum_product = fields.Integer(string="Save Maximum Viewed Product(s)")
    wk_show_product = fields.Integer(string="Show Number of Product(s)")

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        if not self.wk_maximum_product or self.wk_maximum_product <= 0:
            raise UserError(_("Invaild value for 'Save Maximum Viewed Product' !!"))

        if not self.wk_show_product or self.wk_show_product <= 0:
            raise UserError(_("Invaild value for 'Show Number of Product(s)' !!"))

        if self.wk_show_product > self.wk_maximum_product:
            raise UserError(_("'Save Maximum Viewed Product' value should not less than the 'Show Number of Product(s)' value !!"))
        self.env['ir.default'].sudo().set('res.config.settings', 'wk_maximum_product', self.wk_maximum_product or 12)
        self.env['ir.default'].sudo().set('res.config.settings', 'wk_show_product', self.wk_show_product or 5)
        return True


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_values_obj = self.env['ir.default']
        wk_maximum_product = ir_values_obj.sudo().get('res.config.settings', 'wk_maximum_product')
        wk_show_product = ir_values_obj.sudo().get('res.config.settings', 'wk_show_product')
        res.update(wk_maximum_product= wk_maximum_product, wk_show_product = wk_show_product)
        return res

# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
# 
#################################################################################

from odoo import api, models, tools
import logging
_logger = logging.getLogger("__name__")

class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'

    @api.multi
    def read(self, fields=None, load='_classic_read'):

        IrDefault = self.env['ir.default'].sudo()
        odoo_text_replacement = IrDefault.get('res.config.settings', "odoo_text_replacement") or 'System'
        result = super(IrActionsActWindow, self).read(fields, load=load)
        for values in result:
            if 'help' in values and values['help']:
                values['help'] = values['help'].replace('Odoo', odoo_text_replacement)
        return result
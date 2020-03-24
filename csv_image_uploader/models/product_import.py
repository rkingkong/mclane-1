# -*- coding: utf-8 -*-
#################################################################################
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
#################################################################################

import odoo
import logging
from odoo.exceptions import UserError, Warning
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, _
import ast
import os

class wk_import_csv(models.Model):
    _inherit = "wk.import.csv"


    @api.model
    def _get_csv_import_model(self):
        csv_model = super(wk_import_csv, self)._get_csv_import_model()
        csv_model.append(['product.product', 'Product with Main Image'])
        return csv_model


    @api.model
    def product_product_validate_values(self,values):
        msg = ""
        res = {'status':False,'msg':'Product Not Found'}
        if 'image_status' in values:
            msg = values.get('id') + values.get('image_status')
            values.pop('image_status')
        if values.get('id'):
            record_obj = self.env['ir.model.data'].xmlid_to_object(values.get('id'))
            if record_obj:
                try:
                    product_id = values.pop('id')
                    record_obj.write(values)
                    res['status'] = True
                    res['msg'] = product_id + ' updated successfully.'
                except Exception as e:
                    _logger.info('=======%r',e)
                    res['msg'] = e
        elif values.get('default_code'):
            record = self.env['product.product'].search([('default_code','=',values.get('default_code'))])
            if record:
                try:
                    default_code = values.pop('default_code')
                    record.write(values)
                    res['status'] = True
                    res['msg'] = default_code + ' updated successfully.'
                except Exception as e:
                    _logger.info('=======%r',e)
                    res['msg'] = e
        return res




    @api.model
    def get_attachment(self):
        if self.csv_model == "product.product":
            try:
                attachment_id = self.env['ir.model.data'].get_object_reference('csv_image_uploader', 'sample_product_zip')[1]
            except ValueError:
                attachment_id = False
            return attachment_id
        else:
            return super(wk_import_csv,self).get_attachment()

    @api.model
    def get_attachment_id(self,vals):
        if vals.get('csv_model') and vals.get('csv_model') == "product.product":
            try:
                attachment_id = self.env['ir.model.data'].get_object_reference('csv_image_uploader', 'sample_product_zip')[1]
            except ValueError:
                attachment_id = False
            return attachment_id
        return super(wk_import_csv, self).get_attachment_id(vals)


    @api.multi
    def product_product_import_csv(self):
        for current_record in self:
            current_record.import_function()
        return True
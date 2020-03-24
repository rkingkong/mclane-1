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
        csv_model.append(['product.image', 'Product with Multi image'])
        return csv_model

    @api.model
    def get_attachment(self):
        if self.csv_model == "product.image":
            try:
                attachment_id = self.env['ir.model.data'].get_object_reference('csv_image_uploader', 'sample_product_image_zip')[1]
            except ValueError:
                attachment_id = False
            return attachment_id
        else:
            return super(wk_import_csv,self).get_attachment()

    @api.model
    def get_attachment_id(self,vals):
        if vals.get('csv_model') and vals.get('csv_model') == "product.image":
            try:
                attachment_id = self.env['ir.model.data'].get_object_reference('csv_image_uploader', 'sample_product_image_zip')[1]
            except ValueError:
                attachment_id = False
            return attachment_id
        return super(wk_import_csv, self).get_attachment_id(vals)

    @api.model
    def product_image_validate_values(self,values):
        res = {'status':False,'msg':'Product Not Found'}
        if 'image_status' in values:
            res['msg'] = values.get('image_status')
            values.pop('image_status')
        elif not (values.get('product_tmpl_id') or values.get('name')):
            res['msg'] = "Product Id or Name Not Found in CSV "
        else:
            record = self.env['ir.model.data'].xmlid_to_object(values.get('product_tmpl_id'))
            if record:
                extra_image = self.env['product.image'].search([('product_tmpl_id','=',record.id),('name','=',values.get('name'))])
                if extra_image:
                    try:
                        values.pop('product_tmpl_id')
                        name = values.pop('name')
                        record.write(values)
                        res['status'] = True
                        res['msg'] = name + ' updated successfully.'
                    except Exception as e:
                        _logger.info('=======%r',e)
                        res['msg'] = e
                else:
                    try:
                        values['product_tmpl_id'] = record.product_tmpl_id.id
                        res['obj'] = self.env['product.image'].create(values)
                        res['status'] = True
                        res['msg'] = name + ' updated successfully.'
                    except Exception as e:
                        _logger.info('=======%r',e)
                        res['msg'] = e
        return res


    @api.multi
    def product_image_import_csv(self):
        for current_record in self:
            current_record.import_function()
        return True
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

import logging
import base64
import csv
import io
import os
import werkzeug
import zipfile
from urllib import request
from urllib.parse import urlparse
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)
try:
    from PIL import Image
except ImportError:
    _logger.warning(
        'Python Imaging not installed, you can use only .JPG pictures !')

opener = request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
request.install_opener(opener)


class WkImportCsv(models.Model):
    _name = "wk.import.csv"
    _description = "Core Module for import csv File."
    _order = 'create_date desc'


    @api.model
    def _get_csv_import_model(self):
        return []

    @api.model
    def get_attachment(self):
        return False

    @api.onchange('csv_model')
    def onchange_csv(self):
        if not self.csv_model:
            self.sample_attachment = False
        else:
            attachment_id = self.get_attachment()
            self.sample_attachment = attachment_id

    @api.model
    def get_attachment_id(self,vals):
        return False


    # indirection to ease inheritance
    _csv_model_selection = lambda self, *args, **kwargs: self._get_csv_import_model(*args, **kwargs)
    name = fields.Char(string="Name", required=True,copy=False, readonly=True, default=lambda self: _('New'))
    csv_model = fields.Selection(_csv_model_selection, string="Select Entity", required=True, default=lambda self: self._context.get('csv_model', 'product.product'))
    csv_file = fields.Binary( 'File', required=True,)
    sample_attachment = fields.Many2one(comodel_name="ir.attachment",string="Sample Zip File", readonly=True)
    state = fields.Selection([('draft','Draft'),('success','Success'),('error','Error')], string="Status", default="draft")
    log_details = fields.Text(string="Log Summary")
    upload_data = fields.Text(string="Uploaded Data")
    

    @api.model
    def create(self, vals):
        if vals.get('csv_file'):
            zip_ref = base64.b64decode(vals['csv_file'])
            zip_input = io.BytesIO(zip_ref)
            if not zipfile.is_zipfile(zip_input):
                raise UserError("Did not find zip file, please select zip file.")
        if vals.get('csv_model') and not vals.get('sample_attachment'):
            vals['sample_attachment'] = self.get_attachment_id(vals)
        vals['name'] =  self.env['ir.sequence'].next_by_code('wk.import.csv')
        return super(WkImportCsv, self).create(vals)


    @api.multi
    def action_import_csv(self):
        for current_record in self:
            csv_model = current_record.csv_model.replace('.','_')
            if hasattr(current_record, '%s_import_csv' % csv_model):
                return getattr(current_record, '%s_import_csv' % csv_model)()

    @api.model
    def read_image(self,image):
        result = {'status':False, 'encoded_string': ""}
        url = False
        path = os.path.abspath(__file__ + "/../../")
        if image.startswith('https://') or image.startswith('http://'):
            img = urlparse(image).path
            ext = os.path.splitext(img)[1]
            request.urlretrieve(image, path + '1' + ext)
            image = path + '1' + ext
            url = True
        file_name = werkzeug.url_unquote(image)
        try:
            with open(file_name, "rb") as image_file:
                result['encoded_string'] = base64.b64encode(image_file.read())
                result['status'] = True
        except Exception as e:
            _logger.info("Exception %r", e)
            result['encoded_string'] = "Image Not Found"
        if url:
            os.remove(path + '1'+ext)
        _logger.info('===result=====%r',result)
        return result


    @api.model
    def read_zip(self):
        zip_ref = base64.b64decode(self.csv_file)
        zip_input = io.BytesIO(zip_ref)
        zip_input.seek(0)
        zip = zipfile.ZipFile(zip_input)
        path = os.path.abspath(__file__ + "/../../")
        
        return zip
        

    @api.multi
    def read_file(self, file, path):
        path_file = path + file
        csv_file = open(path_file)
        reader = csv.DictReader(csv_file)
        return list(reader)


    def unzip_csv_data(self):
        zip_file = self.read_zip()
        outfile_path = os.path.abspath(__file__ + "/../../") + '/temp/'
        zip_file.extractall(outfile_path)
        return zip_file, outfile_path

    def get_image_folder_path(self,zip_file):
        filenames = zip_file.namelist()
        path = os.path.abspath(__file__ + "/../../")
        path = path + "/temp/" +filenames[0]
        return path

    def get_csv_list(self,zip_file):
        filenames = zip_file.namelist()
        path = os.path.abspath(__file__ + "/../../")
        path = path + "/temp/" +filenames[0]
        data_lst = []
        for file in os.listdir(path):
            if file.endswith(".csv"):
                data = self.read_file(file,path)
                data_lst.append(data)
        return data_lst


    @api.model
    def import_function(self):
        message = ''
        status = True
        for current_record in self:
            csv_model = current_record.csv_model.replace('.','_')
            zip_file,file_name= self.unzip_csv_data()
            data_lst = self.get_csv_list(zip_file)
            path = self.get_image_folder_path(zip_file)
            upload_data = []
            for data in data_lst:
                if not data:
                    raise UserError("You Csv File is Blank.")
                for item in data:
                    image_name = ''
                    values = item
                    res = False
                    values, image_name = current_record.validate_image(values, path)
                    if hasattr(self, '%s_validate_values' % csv_model):
                        res = getattr(self, '%s_validate_values' % csv_model)(values)
                        if not res.get('status'):
                            status = False
                    message += res.get('msg') + '\n'
                    item['image'] = image_name
                    upload_data.append(item)
            current_record.upload_data = upload_data
            current_record.log_details = message
            if status:
                current_record.state = 'success'
            else:
                current_record.state = 'error'


    @api.model
    def validate_image(self, values, path):
        res = False
        image_name = ''
        if values.get('image'):
            image_name = values.get('image')
            if image_name.find('/') < 0:
                image = path +  'images/' + values.get('image') 
            else:
                image = values.get('image')
            result = self.read_image(image)
            if result.get('status'):
                values['image'] = result.get('encoded_string')
            else:
                values['image_status'] = result.get('encoded_string')
        
        return values, image_name






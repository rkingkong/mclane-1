# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models
from odoo import tools
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
class WebsiteBannerImages(models.Model):
	_name = "website.banner.images"
	_order = "sequence asc"

	name = fields.Char('Name', required=True)
	image = fields.Binary(string='Image', required=True)
	thumbnail = fields.Binary(string="Icon")
	link = fields.Char(string = "URL Link", required=False, default=False)
	lang = fields.Many2one('res.lang', string='Language', domain="[('active','=', True)]")
	sequence = fields.Integer(string='Sequence', required=True, default=1)
	state = fields.Selection([('draft','Draft'),('published','Published')], string="State", default="draft")
	
	@api.multi
	def set_to_publish(self):
		for record in self:
			record.state = 'published'

	@api.multi
	def set_to_draft(self):
		for record in self:
			record.state = 'draft'

class Website(models.Model):
	_inherit = "website"
	
	@api.model
	def get_website_banner_images(self):
		lang = request.context.get('lang')
		ir_default = self.env['ir.default'].sudo()
		wk_banner_ids = ir_default.get('website.banner.config', 'wk_banner_ids') or []
		lang_flag = ir_default.get('website.banner.config', 'lang_flag')
		if lang and lang_flag:
			image_ids = self.env['website.banner.images'].sudo().search([('state','=','published'),('lang.code','=',lang),('id','in',wk_banner_ids)])
		else:
			image_ids = self.env['website.banner.images'].sudo().search([('state','=','published'),('id','in',wk_banner_ids)])
		if image_ids:
			return image_ids
		return False

	def get_website_banner_type(self):
		ir_values = self.env['ir.default']
		website_banner_type = ir_values.sudo().get('website.banner.config', 'website_banner_type')
		return website_banner_type
	
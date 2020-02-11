# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models, _
from odoo.http import request 
import logging
_logger = logging.getLogger(__name__)
class WebsiteBanner(models.TransientModel):

	_inherit = 'webkul.website.addons'
	_name = 'website.banner.config'
	
	website_banner_type = fields.Selection([('default','Pagination'),('gallery','Gallery')], string="Banner Type",default="default")
	wk_banner_ids = fields.Many2many(string ="Website Banners",	comodel_name='website.banner.images')
	lang_flag = fields.Boolean(string="Show Banners on the basis of Language", default=False)
	
	@api.multi
	def set_values(self):
		res = super(WebsiteBanner, self).set_values()
		IrDefault = self.env['ir.default'].sudo()
		IrDefault.set('website.banner.config', 'website_banner_type',self.website_banner_type)
		IrDefault.set('website.banner.config', 'wk_banner_ids',self.wk_banner_ids.ids)
		IrDefault.set('website.banner.config', 'lang_flag',self.lang_flag)
		return True

	@api.multi
	def get_values(self):
		res = super(WebsiteBanner, self).get_values()
		IrDefault = self.env['ir.default'].sudo()
		res.update({
			'website_banner_type':IrDefault.sudo().get('website.banner.config', 'website_banner_type'),
			"wk_banner_ids"     :[banner.id for banner in self.env["website.banner.images"].search([("id","in",IrDefault.sudo().get('website.banner.config', 'wk_banner_ids'))])],
			'lang_flag'			:IrDefault.get('website.banner.config', 'lang_flag')
		
		})			
		return res

	@api.model
	def wk_set_demo_banner_config(self):
	
		IrDefault = self.env['ir.default'].sudo()
		banner1=self.env.ref('website_banner_slider.banner_1')
		banner2=self.env.ref('website_banner_slider.banner_2')
		banner3=self.env.ref('website_banner_slider.banner_3')
		banner4=self.env.ref('website_banner_slider.banner_4')
		banner5=self.env.ref('website_banner_slider.banner_5')
		if banner1 and banner2 and banner3 and banner4 and banner5:
			IrDefault.set('website.banner.config', 'wk_banner_ids', [banner1.id,banner2.id,banner3.id,banner4.id,banner5.id])
			
		IrDefault.set('website.banner.config', 'website_banner_type', 'default')
		IrDefault.set('website.banner.config', 'lang_flag', False)
		
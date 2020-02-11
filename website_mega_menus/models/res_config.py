# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)

class MegaMenuConfig(models.TransientModel):

	_inherit = 'webkul.website.addons'
	_name = 'mega.menu.config'

	display_text_header = fields.Boolean(
		string="Show Mega Menu Header"
	)

	mega_menu_header_text = fields.Char(
		string="Header Text",
		help="Text to be displayed on the Mega menu header"
	)
	mega_menu_header_color = fields.Char(
		string="Header Text Color",
		help="Background color to be displayed on the Mega menu header"
	)
	mega_menu_header_bg = fields.Char(
		string="Header Background Color",
		help="Text color to be displayed on the Mega menu header"
	)
	mega_menu_body_bg = fields.Char(
		string="Body Background Color",
		help="Background color to be displayed on the Mega menu body"
	)
	mega_menu_body_color = fields.Char(
		string="Body Text Color",
		help="Text color to be displayed on the Mega menu body"
	)
	root_categ_color = fields.Char(
		string="Root Category Text Color",
		help="Text color to be displayed on the Mega menu root category"
	)
	mega_menu_type = fields.Selection(
		selection=[('default','Dropdown'),('fly_out','Fly Out')],
		string="Menu Type",
		default='default'
	)

	@api.multi
	def get_values(self):
		res = super(MegaMenuConfig, self).get_values()
		IrDefault = self.env['ir.default'].sudo()
		res.update({
			'display_text_header':IrDefault.get('mega.menu.config','display_text_header'),
			'mega_menu_header_text':IrDefault.get('mega.menu.config', 'mega_menu_header_text'),
			'mega_menu_header_color':IrDefault.get('mega.menu.config', 'mega_menu_header_color'),
			'mega_menu_header_bg':IrDefault.get('mega.menu.config', 'mega_menu_header_bg'),
			'mega_menu_body_bg':IrDefault.get('mega.menu.config', 'mega_menu_body_bg'),
			'mega_menu_body_color':IrDefault.get('mega.menu.config', 'mega_menu_body_color'),
			'root_categ_color':IrDefault.get('mega.menu.config', 'root_categ_color'),
			'mega_menu_type':IrDefault.get('mega.menu.config', 'mega_menu_type'),
		})
		return res

	@api.multi
	def set_values(self):
		super(MegaMenuConfig, self).set_values()
		IrDefault = self.env['ir.default'].sudo()
		IrDefault.set('mega.menu.config','display_text_header', self.display_text_header)
		IrDefault.set('mega.menu.config','mega_menu_header_text', self.mega_menu_header_text)
		IrDefault.set('mega.menu.config','mega_menu_header_color', self.mega_menu_header_color)
		IrDefault.set('mega.menu.config','mega_menu_header_bg', self.mega_menu_header_bg)
		IrDefault.set('mega.menu.config','mega_menu_body_bg', self.mega_menu_body_bg)
		IrDefault.set('mega.menu.config','mega_menu_body_color', self.mega_menu_body_color )
		IrDefault.set('mega.menu.config','root_categ_color', self.root_categ_color)
		IrDefault.set('mega.menu.config','mega_menu_type', self.mega_menu_type)
		view = self.env['ir.ui.view'].search([('key','=','website_mega_menus.mega_menu_wk_li2')])
		if (self.mega_menu_type == "fly_out"):
			view.write({'active' :True})
		else:
			view.write({'active' :False})
		return True

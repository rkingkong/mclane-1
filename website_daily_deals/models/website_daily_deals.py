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

from odoo import api, fields, models
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class ProductPricelistItem(models.Model):
	_inherit = "product.pricelist.item"

	website_deals_m2o = fields.Many2one('website.deals', 'Corresponding Deal', help="My Deals", ondelete="cascade")
	actual_price = fields.Float(string='Actual Price')
	discounted_price = fields.Float('Discounted Price',default=0.0)
	website_size_x = fields.Integer('Size X',default=2)
	website_size_y = fields.Integer('Size Y',default=2)
	deal_applied_on = fields.Selection([('1_product', 'Product'),('0_product_variant', 'Product Variant')], "Apply On", help='Pricelist Item applicable on selected option')


	@api.onchange('deal_applied_on','product_tmpl_id','product_id')
	def onchange_deal_applied_on(self):
		self.applied_on = self.deal_applied_on
		self.min_quantity = 1
		self._update_actual_price()

	@api.model
	def _update_actual_price(self):
		if self.applied_on=="1_product":
			self.actual_price = self.product_tmpl_id.list_price
		elif self.applied_on=="0_product_variant":
			self.actual_price = self.product_id.lst_price
		else:
			self.actual_price = 0.0
		self.discounted_price = 0.0



class WebsiteDeals(models.Model):
	_name = 'website.deals'
	_description = 'Website Deals'
	_order = "id desc"

	@api.model
	def _get_default_pricelist(self):
		irDefault = self.env['ir.default'].sudo()
		deal_pricelist = irDefault.get('website.daily.deals.conf', 'deal_pricelist')
		return deal_pricelist

	name = fields.Char(string = 'Name', required=True)
	title = fields.Char(string = 'Title', required=True, help="title of the deal to show in website",default="Get a heavy discount on this season")
	show_title = fields.Boolean('Show Title In Website', help="the title will be displayed in the website and it is displayed only if 'What to Display in Website = Products Only'")
	description = fields.Text(string = 'Description' , help="description of the deal to show in website")
	state = fields.Selection([('draft','Draft'),('validated','In Progress'),('expired','Expired'),('cancel','Cancelled')],'State', default='draft')
	deal_pricelist = fields.Many2one('product.pricelist','Pricelist',required=True,default=_get_default_pricelist)
	overide_config = fields.Boolean('Override Default Configuration')

	start_date = fields.Datetime('Start Date', required=True, default=datetime.now()+ timedelta(days=-1))
	end_date = fields.Datetime('End Date', required=True, default=datetime.now() + timedelta(days=1))

	banner = fields.Binary('Banner', required=False)
	pricelist_items  = fields.One2many(comodel_name = 'product.pricelist.item', inverse_name ='website_deals_m2o' ,string='Products')
	display_products_as = fields.Selection([('grid','Grid'),('slider','Slider')],'How to display Products in Website', default='grid', help="choose how to display the produts in website.")
	item_to_show = fields.Selection([('banner_only','Banner Only'),('products_only','Products Only'), ('both','Both')],'What to Display in Website', default='both', help="choose what you want to display in website.")

	show_message_before_expiry = fields.Boolean('Show Message before Expiry',help="Do you want to show a message before the expiry date of the deal, if yes then set this true.")
	message_before_expiry = fields.Char('Message before Expiry', help="The message you want to show in the website when deal is about to expire.",default='Hurry Up!!! This deal is about to expire.')
	interval_before = fields.Integer('Time interval before to display message' , help="How much time before the expiry date you want to display the message.",default=1)
	unit_of_time = fields.Selection([('minutes','Minutes'),('hours','Hours'),('days','Days'),('weeks','Weeks')],'Time Unit',required=True, default='hours')

	show_message_after_expiry = fields.Boolean('Show Message After Expiry', help="Do you want to show the message after the expiry date of the deal.")
	message_after_expiry = fields.Char('Message After Expiry', help="The message you want to show in the website when deal is expired.",default='Opps!! This deal has been expired.')
	d_state_after_expire = fields.Selection([('blur','Blur'),('delete','Delete')],'What to do with deal after Expiry', default='blur', help="What do you want to do with deal after expiration.Either you can blur the deals in website or delete a deal from website")

	cron_id = fields.Many2one("ir.cron",readonly=True)
	
	@api.multi	
	def create_deal_cron(self):
		model = self.env['ir.model'].sudo().search([('model','=','website.deals')])
		name = self.name or "new"
		val = {
			"name":"website Deal Cron (" + name +  ")",
			"active" :True,
			"user_id": self.env.user.id,
			"numbercall":1,
			"doall":1,
			"model_id": model.id,
			"state":"code",
			"code":"model._check_deal_expiry_cron()",
			"interval_number": False,
			"interval_type":False,
			"nextcall":self.end_date,
		}
		return self.env["ir.cron"].create(val)
		
	@api.multi
	def update_cron(self):
		if self.cron_id:
			name = self.name or "new"
			self.cron_id.name = "website Deal Cron (" + name + ")"
			self.cron_id.numbercall = 1
			self.cron_id.active = self.state == "validated" 
			self.cron_id.nextcall = self.end_date
		else:
			cron = self.create_deal_cron()
			if cron:
				self.cron_id = cron.id
			else:
				UserError("Unable to create crone for the deal!!! Deal will not auto expire.")

	@api.model
	def create(self,vals):
		if not vals.get('banner'):
			raise UserError('No banner chosen, please choose a banner before saving.')
		return super(WebsiteDeals , self).create(vals)

	def unlink(self):
		self.cron_id.unlink()
		return super(WebsiteDeals , self).unlink()
		

	@api.model
	def _update_deal_items(self):
		pricelist = self.deal_pricelist
		if pricelist and self.state=='validated':
			for item in self.pricelist_items:
				item.pricelist_id = pricelist.id
				if item.applied_on=='1_product':
					d_price = pricelist.get_product_price(item.product_tmpl_id,1,None)
					a_price = item.product_tmpl_id.list_price
				elif item.applied_on=='0_product_variant':
					d_price = pricelist.get_product_price(item.product_id,1,None)
					a_price = item.product_id.lst_price
				else:
					d_price = a_price = 0.0
					
				item.discounted_price = d_price
				item.actual_price = a_price
		else:
			for item in self.pricelist_items:
				item.pricelist_id = None
		
		

	@api.onchange('interval_before')
	def onchange_deal_interval_before(self):
		if self.interval_before == 0:
			self.interval_before = 1

	@api.onchange('deal_pricelist','start_date','end_date','overide_config','pricelist_items')
	def onchange_deal_config(self):
		self.state = 'draft'
		self._update_deal_items()

	@api.multi
	def set_to_draft(self):
		self.state = 'draft'
		self._update_deal_items()
		self.update_cron()

	@api.multi
	def set_to_expired(self):
		self.state = 'expired'
		self._update_deal_items()

	@api.multi
	def button_validate_the_deal(self):
		start_date = datetime.strptime(self.start_date,"%Y-%m-%d %H:%M:%S")
		end_date =  datetime.strptime(self.end_date,"%Y-%m-%d %H:%M:%S")
		if start_date > end_date:
			raise UserError('End date can not be earlier than start date.')
		elif end_date > datetime.now():
			if not self.pricelist_items:
				raise UserError('Please add atleast on product in the deal')
			else: 
				self.state = 'validated'
				self._update_deal_items()
				self.update_cron()
		else:
			self.set_to_expired()


	@api.multi
	def cancel_deal(self):
		self.state = 'cancel'
		self._update_deal_items()
		self.update_cron()

	@api.model
	def get_valid_deals(self):
		return self.search(['|',('state','=','validated'),('state','=','expired')]).sorted(lambda d:d.state=="expired")

	@api.model
	def get_page_header(self):
		irDefault = self.env['ir.default'].sudo()
		show_header = irDefault.get('website.daily.deals.conf', 'show_page_header')
		return show_header and irDefault.get('website.daily.deals.conf', 'page_header_text')

	@api.model
	def is_deal_banner_shown(self):
		if self.overide_config:
			return self.item_to_show == 'banner_only' or self.item_to_show == 'both'
		else:
			config_value = self.env['ir.default'].sudo().get('website.daily.deals.conf', 'item_to_show')
			return config_value == 'banner_only' or config_value == 'both'
		return False

	# @api.multi
	# def button_apply_this_pricelist(self):
	# 	msg = "By applying this pricelist the currently applied pricelist of website will be removed and this pricelist will be active on current website."
	# 	return self.show_msg_wizard(msg)


	def show_msg_wizard(self, msg):
		res_id=self.env['deal.wizard.message'].create({'msg':msg})
		modal =  {
                'domain': "[]",
                'name': 'Warning',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'deal.wizard.message',
                'type': 'ir.actions.act_window',
                # 'context': {'feature_id': feature.id},
                'res_id':res_id.id,
                'view_id': self.env.ref('website_daily_deals.website_deal_wizard_pricelist_warning_form_view').id,
                'target': 'new',
        }
		return modal


	@api.model
	def is_deal_product_shown(self):
		if self.overide_config:
			return self.item_to_show == 'products_only' or self.item_to_show == 'both'
		else:
			config_value = self.env['ir.default'].sudo().get('website.daily.deals.conf', 'item_to_show')
			return config_value == 'products_only' or config_value == 'both'
		return False

	@api.model
	def get_display_products_as(self):
		if self.overide_config:
			return self.display_products_as
		else:
			config_value = self.env['ir.default'].sudo().get('website.daily.deals.conf', 'display_products_as')
			return config_value
		return "grid"

	@api.model
	def state_after_expiration(self):
		if self.overide_config:
			return self.state =='expired' and  self.d_state_after_expire
		else:
			config_value = self.env['ir.default'].sudo().get('website.daily.deals.conf', 'd_state_after_expire')
			return self.state =='expired' and config_value and 'blur'
		return False


	@api.model
	def get_message_before_expiry_and_offset(self):
		message = False
		td = False
		end_date =  datetime.strptime(self.end_date,"%Y-%m-%d %H:%M:%S")
		if self.state=="validated":
			if self.overide_config:
				if self.show_message_before_expiry:
					message =  self.message_before_expiry
					interval =  self.interval_before
					unit 	=  self.unit_of_time
					td = self.get_time_delta(interval,unit)
			else:
				IrDefault = self.env['ir.default'].sudo()
				if IrDefault.get('website.daily.deals.conf', 'show_message_before_expiry'):
					message = IrDefault.get('website.daily.deals.conf', 'message_before_expiry')
					interval = IrDefault.get('website.daily.deals.conf', 'show_message_before_expiry')
					unit = IrDefault.get('website.daily.deals.conf', 'show_message_before_expiry')
					td = self.get_time_delta(interval,unit)

		return {'message':message,'offset':td and end_date - td }
	@api.model
	def get_time_delta(self,interval,unit):
		if interval and unit:
			if unit=="minutes":
				td = timedelta(minutes=int(interval))
			elif unit=="hours":
				td = timedelta(hours=int(interval))
			elif unit=="days":
				td = timedelta(days=int(interval))
			elif unit=="weeks":
				td = timedelta(weeks=int(interval))
			elif unit=="months":
				td = timedelta(months=int(interval))
			else:
				td = timedelta(hours=1)
			return td
		return False

	@api.model
	def get_message_after_expiry(self):
		message = False
		if self.state=="expired":
			if self.overide_config:
				message =  self.show_message_after_expiry and self.message_after_expiry
			else:
				IrDefault = self.env['ir.default'].sudo()
				message = IrDefault.get('website.daily.deals.conf', 'show_message_after_expiry') and IrDefault.get('website.daily.deals.conf', 'message_after_expiry')
		return message
	
	@api.multi
	def _check_deal_expiry_cron(self):
		valid_deals = self.get_valid_deals()
		for deal in valid_deals:
			deal.button_validate_the_deal()


class ProductTemplate(models.Model):
	_inherit = "product.template"
	
	def write(self, vals):
		res = super(ProductTemplate, self).write(vals)
		if vals.get('list_price'):
			deals = self.env['website.deals'].get_valid_deals()
			for deal in deals:
				deal._update_deal_items()
		return res

class ProductTemplateAttributeValue(models.Model):
	_inherit = "product.attribute.value"

	def write(self, vals):
		res = super(ProductTemplateAttributeValue, self).write(vals)
		if vals.get('price_extra'):
			deals = self.env['website.deals'].get_valid_deals()
			for deal in deals:
				deal._update_deal_items()
		return res
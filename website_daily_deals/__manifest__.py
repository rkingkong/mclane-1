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
{
  "name"                 :  "Website Daily Deals and Flash Sales",
  "summary"              :  "Website Daily Deals and Flash Sales allows you to create and manage daily exciting deals in your Odoo website.",
  "category"             :  "Website",
  "version"              :  "3.0.1",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Daily-Deals.html",
  "description"          :  """Website Daily Deals and Flash Sales
Website Daily Deals
Odoo Website Daily Deals and Flash Sales
Odoo Website Daily Deals
Daily Deals
Flash Deals
Flash Daily Deals
Odoo Website Daily Deals
Daily Offers
Create Daily Offers
Manage Daily Offers
Per day deal
Per day discount
Flash Discount on Odoo Website
Odoo Website Flash Discount
Odoo website Flash Deals""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_daily_deals",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                             'stock',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'view/website_daily_deals_view.xml',
                             'view/config_view.xml',
                             'view/webkul_addons_config_inherit_view.xml',
                             'view/templates.xml',
                            ],
  "demo"                 :  ['data/demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  99,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}

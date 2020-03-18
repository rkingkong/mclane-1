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
  "name"                 :  "Website Buy Now",
  "summary"              :  "Odoo website Buy Now module adds a Buy Now button to the products on Odoo website so you buy the products in a single click.",
  "category"             :  "Website",
  "version"              :  "1.0.1",
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Buy-Now.html",
  "description"          :  """Odoo website Buy Now
Buy it Now
Buy Now Button
Buy Now products
Odoo buy Now
Buy now website
Buy now with i click
Buy now with one click
Buy now icon
Odoo website Buy Again
Previous Purchases
Old orders
Previous products
Buy products again
Old products again
Previous orders
Order again""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_buy_now",
  "depends"              :  [
                             'website_sale',
                             'sale',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/templates.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  69,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
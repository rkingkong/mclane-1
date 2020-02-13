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
  "name"                 :  "Website Buy Again",
  "summary"              :  "With Odoo Website Buy Again the customers can easily buy the previously bought products in a click. The module adds a tab BUY AGAIN on the Odoo website. The tab has list of previously bought products.",
  "category"             :  "Website",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/odoo-website-buy-again.html",
  "description"          :  """Odoo website Buy Again
Previous Purchases
Old orders
Previous products
Buy products again
Old products again
Previous orders
Order again
""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_buy_again&custom_url=/buy_again",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/buy_again_template.xml',
                             'views/buy_again_config_view.xml',
                             'views/buy_again_snippet.xml',
                            ],
  "demo"                 :  ['data/website_buy_again_demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  25,
  "currency"             :  "EUR",
  "pre_init_hook"        :  "pre_init_check",
}
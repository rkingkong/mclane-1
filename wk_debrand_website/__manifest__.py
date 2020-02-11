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
  "name"                 :  "Odoo Website Debranding",
  "summary"              :  "This is a debranding module for Odoo-Website.",
  "category"             :  "Extra Tools",
  "version"              :  "1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com",
  "description"          :  "Odoo Website Debranding",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=wk_debrand_website&version=11.0",
  "depends"              :  ['website','wk_debrand_odoo'],
  "data"                 :  [
                                'views/website_templates.xml',
                                'views/website_view.xml',
                                'data/web_planner_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  39,
  "currency"             :  "EUR",
}
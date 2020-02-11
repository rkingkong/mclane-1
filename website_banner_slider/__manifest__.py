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
  "name"                 :  "Website Banner Slider",
  "summary"              :  "The module allows you to display sliding banners on the website page. The banner sliders can be designed in the Odoo backend.",
  "category"             :  "Website",
  "version"              :  "1.2.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-Banner-Slider.html",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=website_banner_slider",
  "depends"              :  [
                             'website_sale',
                             'website_webkul_addons',
                            ],
  "data"                 :  [
                             'view/website_banner_image_view.xml',
                             'view/res_config_view.xml',
                             'view/templates.xml',
                             'security/ir.model.access.csv',
                            ],
  "demo"                 :  ['data/demo.xml'],
  "images"               :  ['static/description/Banner.png'],
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  19,
  "currency"             :  "EUR",
}
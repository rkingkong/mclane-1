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
  "name"                 :  "CSV Image Uploader",
  "summary"              :  "This module helps to import images for Product Variants, Product Extra Images, and Website Product Categories.",
  "category"             :  "Marketing",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "http://www.webkul.com",
  "description"          :  """This module helps to import images for Product Variants, Product Extra Images, and Website Product Categories.""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=csv_image_uploader&version=11.0",
  "depends"              :  [
                             'sale_management',
                             'website_sale',
                            ],
  "data"                 :  [
                             'views/import_csv_view.xml',
                             'views/csv_sequence.xml',
                             'data/demo_data.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  "pre_init_hook": "pre_init_check",

}
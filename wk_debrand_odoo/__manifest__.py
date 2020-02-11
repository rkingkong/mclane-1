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
  "name"                 :  "Odoo Backend Debranding",
  "summary"              :  "Odoo Backend Debranding allows you to change or remove the logo, favicon, page title, and text from the Odoo backend.",
  "category"             :  "Extra Tools",
  "version"              :  "1.0.8",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Backend-Debranding.html",
  "description"          :  """Debranding
Unbranding
Debranding in Odoo
Debranding in Odoo Backend
Odoo Backend Debranding
Backend Debranding in Odoo
Backend Debranding
Odoo Backend Unbranding 
de-corporatizing
White label
Backend Unbranding """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=wk_debrand_odoo",
  "depends"              :  [
                             'web',
                             'mail',
                            ],
  "data"                 :  [
                             'views/res_config_view.xml',
                             'views/web_client_template.xml',
                             'views/templates.xml',
                            ],
  "demo"                 :  ['data/demo.xml'],
  "qweb"                 :  [
                             'static/src/xml/base.xml',
                             'static/src/xml/client_action.xml',
                             'static/src/xml/dashboard.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  30,
  "currency"             :  "EUR",
}
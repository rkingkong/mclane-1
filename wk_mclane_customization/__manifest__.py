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
  "name"                 :  "Mclane Customization Depends",
  "summary"              :  """This module provides functionality to auto send email to customers before 15 days of license expiration""",
  "category"             :  "Website",
  "version"              :  "1.0.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/",
  "depends"              :  [
                             'mclane_customization'
                            ],
  "data"                 :  [
                             'edi/license_expiry_alert_mail.xml',
                             'views/license_expiry_alert_cron.xml'
                            ],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
}
# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
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

from odoo import models, fields, api
import datetime
import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def send_license_expiration_alert_mail(self):
        today = datetime.date.today()
        expected_date = today + datetime.timedelta(days=15)
        expected_date = expected_date.strftime('%Y-%m-%d')

        obj = self.search(['|', '|',('expiration_date_cig','=',expected_date),('expiration_date_sale','=',expected_date),('expiration_date_tc','=',expected_date)])
        template_id = self.env.ref('wk_mclane_customization.license_expiration_alert_email')
        for rec in obj:
            template_id.send_mail(rec.id, force_send=True)
        return True

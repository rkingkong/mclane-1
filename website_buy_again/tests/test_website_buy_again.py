# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo.tests import common

class Test_Buy_again_config(common.TransactionCase):
    def setUp(self):
        super(Test_Buy_again_config, self).setUp()
        web_rec = self.env['website'].browse(1)
        self.record = self.env['buy.again.config'].create({
        'name': 'Demo_setting',
        'website_id': web_rec.id,
        'product_limit':10,
        'menu_buy_again':'Buy Again',
        'set_active':True,
        })

    def test_toggle_set_active(self):
        self.assertTrue(self.record.set_active)

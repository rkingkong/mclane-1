# -*- coding: utf-8 -*-
#################################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>;)
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
# If not, see <https://store.webkul.com/license.html/>;
#################################################################################
{
    "name"                 :  "Best selling products",

    "summary"              :  "Best selling products",

    "description"          :  "Best selling products",

    "author"               :  "Webkul Software Pvt. Ltd.",
    "license"              :  "Other proprietary",
    "website"              :  "http://www.webkul.com",
    "category"             :  "Website",
    "version"              :  "1.0.0",
    "depends"              :  ["website_sale"],
    "data"                 :  [
                                'data/best_selling_cron.xml',
                                'views/assets.xml',
                                'views/templates.xml',
                                'views/product_public_category.xml',
                                'views/res_config.xml',
                                ],
    "qweb"                 :  [],
    "application"          :  True,
    "installable"          :  True,
    # "images"               :  ['static/description/banner.png'],
    # "price"                :  99.0,
    "currency"             :  "EUR",
    "pre_init_hook"        :  "pre_init_check",
}

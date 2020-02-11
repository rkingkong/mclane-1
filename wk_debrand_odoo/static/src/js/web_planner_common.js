/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define('wk_debrand_odoo.web.planner.common', function (require) {
    "use strict";
    var planner_dialog= require('web.planner.common');

    planner_dialog.PlannerDialog.include({
        _display_page: function (page_id) {
            var self = this;
            var odoo_text_replacement="";
            var page_href = '#'+page_id;
            self._super(page_id);
            if(page_id && $(page_href).html()){
                if(odoo.debranding_settings && odoo.debranding_settings.odoo_text_replacement) 
                    odoo_text_replacement = odoo.debranding_settings.odoo_text_replacement;
                var text = $(page_href).html().replace(/odoo/ig,odoo_text_replacement);
                $(page_href).html(text);
            }
        },
    });
});
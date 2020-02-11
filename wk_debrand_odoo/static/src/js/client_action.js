/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define('wk_debrand_odoo.client_action', function (require) {
    "use strict";
    require('mail.chat_client_action');
    var core = require('web.core');

    core.action_registry.get('mail.chat.instant_messaging').include({
        init: function(parent, action, options){
            var self = this;
            var options = options ||{};
            options.odoo_text_replacement="";
            if(odoo.debranding_settings && odoo.debranding_settings.odoo_text_replacement) 
                options.odoo_text_replacement = odoo.debranding_settings.odoo_text_replacement.trim();
            this._super(parent, action, options);
        }
    });
});
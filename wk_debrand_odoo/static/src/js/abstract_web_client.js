/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
/* License URL : <https://store.webkul.com/license.html/> */

odoo.define('wk_debrand_odoo.abstract_web_client', function (require) {
"use strict";
    var abstractwebclient = require("web.AbstractWebClient")
    var rpc = require('web.rpc')
    
    abstractwebclient.include({
        init: function(parent) {
            this._super(parent);
            var self = this;
            rpc.query({model: 'res.config.settings',method: 'get_debranding_settings',}).done(function(debranding_settings){
                odoo.debranding_settings = debranding_settings;
                self.set('title_part', {"zopenerp": debranding_settings.title_brand && debranding_settings.title_brand.trim() || ''});
            });
        },
    });
});
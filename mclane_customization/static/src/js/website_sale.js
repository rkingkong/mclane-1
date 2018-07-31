odoo.define('mclance_customization.website_sale', function (require) {
    "use strict";

    var core = require('web.core');
    $(document).ready(function () {

        $("input[name='expiration_date_cig']").change(function() {
            $("input[name='no_expiration_date_cig']").attr('checked', false);
        });
        $("input[name='expiration_date_tc']").change(function() {
            $("input[name='no_expiration_date_tc']").attr('checked', false);
        });
        $("input[name='expiration_date_sale']").change(function() {
            $("input[name='no_expiration_date_sale']").attr('checked', false);
        });


        $("input[name='no_expiration_date_cig']").change(function() {
            $("input[name='expiration_date_cig']").val('')
        });
        $("input[name='no_expiration_date_tc']").change(function() {
            $("input[name='expiration_date_tc']").val('')
        });
        $("input[name='no_expiration_date_sale']").change(function() {
            $("input[name='expiration_date_sale']").val('')
        });
    });

})

odoo.define('mclance_customization.website_sale', function (require) {
    "use strict";

    var core = require('web.core');

    $(document).ready(function () {
    $('#product_detail .quantity').change(function(){
        var $input = $(this);
        var qty = $(this).val()
        var margin_val = parseFloat($('#oe_margin_hide').text())
        $('#oe_margin > .oe_currency_value').text(parseFloat(margin_val*parseInt(qty)).toFixed(2))
    })

	$('a.page-scroll').bind('click', function(event) {
		var $anchor = $(this);
		$('html, body').stop().animate({
		    scrollTop: ($($anchor.attr('href')).offset().top - 50)
		}, 1250, 'easeInOutExpo');
		event.preventDefault();
	    });

	    // Highlight the top nav as scrolling occurs
	    $('body').scrollspy({
		target: '.navbar-fixed-top',
		offset: 51
	    });

	    // Offset for Main Navigation
	    $('#mainNav').affix({
		offset: {
		    top: 100
		}
	    });

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

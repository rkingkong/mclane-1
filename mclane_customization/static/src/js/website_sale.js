odoo.define('mclance_customization.website_sale', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var ajax = require('web.ajax');

    $(document).ready(function () {

    var product_name = $('#product_name_attachemnt').val()
    $("#learn_more").on('click', function(event){
        ajax.jsonRpc("/shop/open_attachment", 'call', {
             'product_id': product_name,
        }).then(function (data) {
            if (data){
                window.open(window.location.origin + "/web/content/" + data, 'new');
            }
        });

    });

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

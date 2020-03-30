odoo.define('website_recently_viewed.website_recently_viewed', function(require) {
    "use strict";

    $(document).ready(function() {
        var number = parseInt($('#show-product').data('show-product'), 10);
        $("#owl-recentaly-viewed").owlCarousel({
            items: number,
            responsive: {
              0: {
                items: 2,
                margin: 10,
                stagePadding: 20,
              },
              768: {
                items: 2,
                margin: 20,
                stagePadding: 50,
              },
              1000: {
                items: 4
              }
            }
        });
        $('.wk_recently_view_container').show();

        $(document).on('click', '.recent-add', function(event) {
            if (!event.isDefaultPrevented()) {
                $(this).closest('form').submit();
            }
        });
    });
});

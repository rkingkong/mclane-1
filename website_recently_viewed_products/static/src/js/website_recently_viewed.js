odoo.define('website_recently_viewed.website_recently_viewed', function(require) {
    "use strict";

    $(document).ready(function() {
        var number = parseInt($('#show-product').data('show-product'), 10);
        $("#owl-recentaly-viewed").owlCarousel({
            items: number
        });
        $('.wk_recently_view_container').show();

        $(document).on('click', '.recent-add', function(event) {
            if (!event.isDefaultPrevented()) {
                $(this).closest('form').submit();
            }
        });
    });
});

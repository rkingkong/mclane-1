$(document).ready(function() {

var owl_pagination = $("#owl-pagination");
        owl_pagination.owlCarousel({
          items : 1, 
          // navigation : true, // Show next and prev buttons
          // slideSpeed : 200,
          smartSpeed:2000,
          
          pagination : true,
          paginationNumbers: true,
          transitionStyle : "fade",
          autoplay:true,
          autoplayTimeout:4000,
          autoplaySpeed:2000,
          loop:true,
          stopOnHover : true,
          itemsDesktop : [2000,1], //5 items between 1000px and 901px
          itemsDesktopSmall : [900,1], // betweem 900px and 601px
          itemsTablet: [600,1], //2 items between 600 and 0
          itemsMobile : false, //
          responsiveRefreshRate : 20000
        });



        var counter = 1;
        $('#owl-pagination .owl-dots .owl-dot').each(function(){
          $(this).find("span").text(counter);
          counter +=1;

        });
        $(".owl-carousel").hover(function(){
          // $(' #owl-pagination .owl-dots').css('visibility','visible');
          owl_pagination.trigger('stop.owl.autoplay')

        },function(){
          // $('#owl-pagination .owl-dots').css('visibility','hidden');
          owl_pagination.trigger('play.owl.autoplay')
        })

  var owl_gallery = $("#owl-gallery");
        
      owl_gallery.owlCarousel({
          items : 1, 
          nav : false, // Show next and prev buttons
          smartSpeed:2000,
          
          pagination : true,
          paginationNumbers: true,
          transitionStyle : "fade",
          
          autoplay:true,
          autoplayTimeout:4000,
          autoplaySpeed:2000,
          loop:true,
          autoplayHoverPause:true,
          itemsDesktop : [2000,1], //5 items between 1000px and 901px
          itemsDesktopSmall : [900,1], // betweem 900px and 601px
          itemsTablet: [600,1], //2 items between 600 and 0
          itemsMobile : false, //
          responsiveRefreshRate : 20000,

          dotsContainer: '#custom',

        });

        // $('.owl-dot').click(function () {
        //   owl_gallery.trigger('to.owl.carousel', [$(this).index(), 1000]);
        // });
        $('.owl-next').click(function () {
          owl_gallery.trigger('next.owl.carousel',[2000]);
        });
        $('.owl-prev').click(function () {
          owl_gallery.trigger('prev.owl.carousel',[2000]);
        });
        $('.owl-dot').click(function () {
          owl_gallery.trigger('to.owl.carousel', [$(this).index(), 2000]);
        });

        $('#custom-nav').hover(function () {
          owl_gallery.trigger('stop.owl.autoplay');
        },function(){
          owl_gallery.trigger('play.owl.autoplay');
        });
        

});
odoo.define('theme_glitter.glitter_snippets_call', function (require)
{
  "use strict";
  var ajax = require('web.ajax');
  var core = require('web.core');

  var QWeb = core.qweb;

  var carouselReset = function(self){
    $(self).find('.best_selling_carousel').trigger('destroy.owl.carousel');
    $(self).find("#best_selling_nav button").remove();
    $(self).find('.owl-item.cloned').remove();
    $(self).find('.best_selling').hide();
  };


  var carouselStart = function(self, products){
    $(self).find('.best_selling_carousel').owlCarousel({
      loop: products.length > 2 ? true : false,
      margin: 30,
      dots: false,
      nav: true,
      navText : products.length > 2 ? ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"] : ["",""],
      navContainer: '#best_selling_nav',
      responsiveClass: true,
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
    // $(self).find("#best_selling_nav").append($(self).find(".owl-nav"));

  };

  var setBestSellingProducts = function(self,products){
    if (products.length > 0){
      carouselReset(self);
      $(self).find('.best_selling').show()

      var html_content = new Array();

      $(products).each(function(){
        var carousel_item =
        '<div class="carousel-item">'+
        '<a href="'+this.url+'">'+
        '<div class="carousel-item-image">'+
        '<img src="data:image/jpeg;base64,'+this.image+'" />'+
        '</div>'+
        '<div class="carousel-item-text">'+
        '<span class="item-kicker">'+this.name+'</span>'+
        '<h3 class="item-title">'+this.curr_symbol+' '+this.price+'</h3>'+
        '</div>'+
        '</a>'+
        '</div>'
        html_content.push(carousel_item)
      })

      $(self).find('.best_selling_carousel').replaceWith(
        '<div class="best_selling_carousel owl-carousel owl-theme">'+
        html_content.join('')+
        '</div>'
      )
      carouselStart(self, products);
    }

    else{
      carouselReset(self);
    }
  };

  var setLatestProducts = function(self, products){

    if(products.length > 0){
      $(self).find('.latest_products').show()
      var html_content = new Array();
      $(products).each(function(){
        var list_item =
        '<a href="'+this.url+'">'+
        '<li class="list-group-item">'+
        '<div class="image-parent">'+
        '<img src="data:image/jpeg;base64,'+this.image+'"class="img-fluid"/>'+
        '</div>'+
        '<div class="details">'+
        '<div class="name">'+
        this.name+
        '</div>'+
        '<div class="price">'+
        this.curr_symbol+' '+this.price+
        '</div>'+
        '</div>'+
        '</li>'+
        '</a>'
        html_content.push(list_item)
      })
      $(self).find(".latest_products ul.list-group").replaceWith(
        '<ul class="list-group">'+
        html_content.join('')+
        '</ul>'
      )
    }
    else{
      $(self).find('.latest_products').hide();
    }
  };

  $(document).ready(function(){
    var self = this
    ajax.jsonRpc('/get_wk_products'+window.location.pathname, 'call', {})
    .then(function(res){
      setBestSellingProducts(self, res['best_selling_products'])
      setLatestProducts(self, res['latest_products'])
    })
  });



  var sAnimation = require('website.content.snippets.animation');

  sAnimation.registry.GlitterSnippets = sAnimation.Class.extend({
    selector: '.best_selling_carousel',

    start: function(){
      $('.best_selling_carousel').owlCarousel({
        loop: true,
        margin: 30,
        dots: true,
        nav: true,
        navContainer: '#best_selling_nav',
        responsiveClass: true,
        responsive: {
          0: {
            items: 2,
            margin: 10,
            stagePadding: 20,
          },
          600: {
            items: 3,
            margin: 20,
            stagePadding: 50,
          },
          1000: {
            items: 4
          }
        }
      });
    },
  });
})

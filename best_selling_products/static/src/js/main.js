odoo.define('theme_glitter.glitter_snippets_call', function (require)
{
  "use strict";
  var ajax = require('web.ajax');
  var core = require('web.core');
  var utils = require('web.utils');

  var website_sale_utils = require('website_sale.utils');
  var concurrency = require('web.concurrency');

  var QWeb = core.qweb;

  var comparelist_product_ids = JSON.parse(utils.get_cookie('comparelist_product_ids') || '[]');
  var product_compare_limit = 4;
  var guard = new concurrency.Mutex();
  var product_data = {}

  var load_products = function(product_ids) {
    var self = this;
    return ajax.jsonRpc('/shop/get_product_data', 'call', {
        'product_ids': product_ids,
        'cookies': JSON.parse(utils.get_cookie('comparelist_product_ids') || '[]'),
    }).then(function (data) {
        comparelist_product_ids = JSON.parse(data.cookies);
        delete data.cookies;
        _.each(data, function(product) {
            product_data[product.product.id] = product;
        });
    });
  };

  var toggle_panel = function() {
    $('#comparelist .o_product_panel_header').popover('toggle');
  };

  var update_comparelist_view = function() {
      $('.o_product_circle').text(comparelist_product_ids.length);
      $('.o_comparelist_button').hide();
      if (_.isEmpty(comparelist_product_ids)) {
          $('.o_product_feature_panel').hide();
          toggle_panel();
      } else {
          $('.o_comparelist_products').show();
          if (comparelist_product_ids.length >=2) {
              $('.o_comparelist_button').show();
              $('.o_comparelist_button a').attr('href', '/shop/compare/?products='+comparelist_product_ids.toString());
          }
      }
  };

  var update_cookie = function(){
    document.cookie = 'comparelist_product_ids=' + JSON.stringify(comparelist_product_ids) + '; path=/';

    update_comparelist_view();
  };

  var update_content = function(product_ids, reset) {
    var self = this;
    if (reset) {
        $('.o_comparelist_products .o_product_row').remove();
    }
    _.each(product_ids, function(res) {
        var $template = product_data[res].render;
        $('.o_comparelist_products').append($template);
    });
  }

  var add_new_products = function(product_id){
      guard.exec(_add_new_products.bind(this, product_id));
    };

  var _add_new_products = function (product_id) {
    var self = this;
    $('.o_product_feature_panel').show();
    if (!_.contains(comparelist_product_ids, product_id)) {
        comparelist_product_ids.push(product_id);
        if(_.has(product_data, product_id)){
            update_content([product_id], false);
        } else {
            return load_products([product_id]).then(function () {
                update_content([product_id], false);
                update_cookie();
            });
        }
    }
    update_cookie();
  };

  var set_to_compare = function($this){
    if (comparelist_product_ids.length < product_compare_limit) {
        var prod = $($this).data('product-product-id');
        if (!prod) {
            return;
        }
        add_new_products(prod);
      } else {
          $('.o_comparelist_limit_warning').show();
          if ((!$('.comparator-popover').length) || true) {
            $('#comparelist .o_product_panel_header').popover('show');
        }
      }
  };

  var update_wishlist_view = function() {
        if (this.wishlist_product_ids.length > 0) {
            $('#my_wish').show();
            $('.my_wish_quantity').text(this.wishlist_product_ids.length);
        }
        else {
            $('#my_wish').hide();
        }
    };

  var add_new_products_wl = function($el, e){
      var self = this;
      var product_id = parseInt($el.data('product-product-id'), 10);
      if (!product_id && e.currentTarget.classList.contains('o_add_wishlist_dyn')) {
          product_id = parseInt($el.parent().find('.product_id').val());
      }
      if (product_id) {
        return ajax.jsonRpc('/shop/wishlist/add', 'call', {
          'product_id': product_id
        }).then(function () {
          // self.wishlist_product_ids.push(product_id);
          // self.update_wishlist_view();
          website_sale_utils.animate_clone($('#my_wish'), $el.closest('form'), 25, 40);
          $el.prop("disabled", true).addClass('disabled');
        });
      }
  };

  //------------------ADD TO CART -------------------------
  // var add_to_cart = function(product_id, qty_id) {
  //   var add_to_cart = ajax.jsonRpc("/shop/cart/update_json", 'call', {
  //     'product_id': parseInt(product_id, 10),
  //     'add_qty': parseInt(qty_id, 10),
  //     'display': false,
  //   });
  //   add_to_cart.then(function(resp) {
  //       if (resp.warning) {
  //         if (! $('#data_warning').length) {
  //             $('.wishlist-section').prepend('<div class="mt16 alert alert-danger alert-dismissable" role="alert" id="data_warning"></div>');
  //         }
  //         var cart_alert = $('.wishlist-section').parent().find('#data_warning');
  //         cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + resp.warning);
  //       }
  //       $('.my_cart_quantity').html(resp.cart_quantity || '<i class="fa fa-warning" /> ');
  //   });
  //   return add_to_cart;
  // };

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
        '<a class="btn btn-default btn-xs o_add_wishlist" '+
        (this.in_wish ? 'disabled' : '') +
        ' title="Add to Wishlist" data-product-product-id='+this.product_varient_id+' data-action="o_wishlist">'+
        '<span class="fa fa-heart">'+
        '</span>'+
        '</a>'+
        '<a class="hidden-xs btn btn-default btn-xs o_add_compare" title="Compare" data-product-product-id='+this.product_varient_id+' data-action="o_comparelist"><span class="fa fa-exchange"></span>'+
        '<input name="product_id" value="'+this.product_id+'" type="hidden"/>'+
        '</a>'+
        //-------------ADD TO CART----------------------------
        // '<a class="btn btn-default btn-xs a-submit">'+
        // '<input name="product_id" value="'+this.product_varient_id+'" type="hidden"/>'+
        // '<span class="fa fa-shopping-cart" />'+
        // '</a>'+
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

      //---------OPTION FEATURE ADD TO CART --------
      // $(".wk_customization a.a-submit").on('click', function(o) {
      //   add_to_cart($(this).find("input").val(), 1).then(function(){
      //     window.location="/shop/cart"
      //   });
      // })

      $(".wk_customization .o_add_wishlist").on('click',function(e){
        add_new_products_wl($(this), e);
      });

      $(".wk_customization .o_add_compare").on('click', function(e){
        set_to_compare(this)
      })
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

odoo.define('website_buy_now.main', function (require) {
  "use strict";
  /* Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
  /* See LICENSE file for full copyright and licensing details. */
  var ajax=require('web.ajax');





  $(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    $("#product_buy_now").on('click', function(event){
      event.preventDefault();
      $('input[name="buy_now"]').val("True");
      localStorage.setItem("buy_now", true);
      $(this).closest('form').submit();
    })



    function ajax_get_quantity(){
      $.get('/buy_now/get-totalquantity').then(function(success){
        var data =  JSON.parse(success);
        var id = $('.my_cart_quantity');
        if (data.total_quantity > 0){id.text(data.total_quantity).show();}
        localStorage.setItem("buy_now", false);
      })
    }

    function loadPage(){
      var path = window.location.pathname;
      var paths = ['/shop/checkout','/shop/payment','/shop/confirmation','/shop/cart','/shop/address']
      if ((localStorage.getItem("buy_now") == 'true' && !paths.includes(path))|| (path == '/shop')){
        $('.my_cart_quantity ').hide();
        ajax_get_quantity();
      }
      if(localStorage.getItem('is_payment_er') == 'true'){
        $("#cart-error").show();
        localStorage.setItem("buy_now", false);
        localStorage.setItem("is_payment_er",false);
      }
    }

    loadPage();

    $('.js_variant_change').on('click',function(event){
      $(this).trigger('change');
      var bool = $("#add_to_cart").attr('class');
      var ele = $("#product_buy_now");
      bool.includes('disable') ? ele.addClass('disabled') : ele.removeClass('disabled');
    })

    var _updateX = true;
    $('#o_payment_form_pay').click(function(event){
        if(_updateX == true){
          _updateX = false;
          var _self = $(this);
          var _ref_p = $('#wk_intg_products');
          var _ref_q = $('#wk_intg_qty');
          if(_ref_p.length > 0 && _ref_q.length > 0){
            event.preventDefault();
            event.stopPropagation();
            ajax.jsonRpc("/buy_now/check/product/integrity", 'call', {"product_id":parseInt(_ref_p.val()), "qty": parseInt(_ref_q.val())},{
              'async': false,
            })
            .then(function(success){
              if (success.redirect==true){
                  localStorage.setItem("buy_now", false);
                  localStorage.setItem("is_payment_er",true);
                  window.location.href = "/shop/cart";
              }else{
                _self.trigger('click');
              }
            })
          }
        }
    });

  })

})

$(document).on('click','#product_buy_now_cart_logo', function(event){
  try {
    event.preventDefault();
    var _self = $(this);
    localStorage.setItem("buy_now", true);
    let product_id = _self.parents('section').find('input[name="product_id"]');
    var _=document.createElement('FORM');
    _.method='POST';
    _.action='/shop/cart/update';
    var _in_1 = event.currentTarget.parentElement.querySelector("#wk_bn_val").cloneNode(true);
    var _in_2 = event.currentTarget.parentElement.querySelector("#wk_bn_id").cloneNode(true);
    _.appendChild(_in_1);
    _.appendChild(_in_2);
    document.body.appendChild(_);
    _.submit();
    event.preventDefault();
  } catch (e) {
    console.log(e);
  }

})

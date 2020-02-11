/* Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>) */
/* See LICENSE file for full copyright and licensing details. */
odoo.define('website_mega_menus.website_mega_menus', function (require) {
    "use strict";
    var base = require('web_editor.base');
    var ajax = require('web.ajax');

        $(document).click(function() {
          $('#fly_out_view').hide();
        });

        function fly_out_view_open(e){
          e.stopPropagation();
          $('#fly_out_view').show();
        }

       $(document).ready(function () {
            $(".hover_mega_menu").parent(".dropdown").parent('.dropdown-menu[role=menu]').addClass("super");
            $('#fly_out_view_open, #fly_out_view .dropdown-menu')
              .on('click', fly_out_view_open)
              .hover(function(e){
                var width = window.innerWidth;
               if (width > 767)
                {
                  fly_out_view_open(e);
                }
              });
            $('#fly_out_view').on('click', function(e){
              $('#fly_out_view').show();
              e.stopPropagation();

            })

            set_selected_menu();

            $('.levelclass').each(function(index) {
                var level = $(this).attr('level')
                $(this).css({'padding-left':6*level+'%'})
            });

            $("#top_menu .dropdown").hover(function(){
               var color = $(this).find('.dropbtn').attr('color')
               var mega_menu = $(this).find('.dropbtn').attr('mega_menu')
               var width = window.innerWidth;
               if (mega_menu == 'True' && width > 767)
               {
                 $(this).find('.dropbtn').css({'border-bottom':'5px solid #'+color+ '' ,'padding-bottom': '10px'})
               }
            }, function() {
                $(this).find('.dropbtn').css({'border-bottom':'none','padding-bottom': '15px'})
            });

            $('.dropbtn').click(function(event){
              event.preventDefault();
              var width = window.innerWidth;
              var href = $(this).attr('href');
              if (width <= 767 && href== "#mega"){
                $(this).parent('li').find('.dropdown-content').toggle();
              }
              else{
                window.location.href = href;
              }
            })

            $('main').click(function() {
              $(".navbar-collapse").collapse('hide');
            })

            $('#top_menu li .dropdown-content').children().find('a').click(function(e){
              localStorage.setItem('default_menu_bar', $(this).parents('li').last().prop('id'));
            })

            $('#top_menu >li >.dropdown-menu[role=menu].super >li >a[href=#mega]').click(function(ev) {
              var width = window.innerWidth;
              if (width < 768){
                ev.stopPropagation();
              }
            })

        });

        function set_selected_menu(){
          try{
            var bool = true;
            $('#top_menu li').each(function() {
              if($(this).prop('class').includes('active')){
                localStorage.setItem('default_menu_bar', '')
                bool = false;
              }
            });
            if(bool === true && window.location.href.includes('/shop/category/')){
              let ref = '#'+localStorage.getItem('default_menu_bar');
              $(ref).addClass('active');
            }
          }catch(e){}

        }

       });

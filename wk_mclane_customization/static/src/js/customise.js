odoo.define('wk_mclane_customization.wk_mclane_customization', function(require) {
    "use strict";

// console.log("sdfadsfasdfasdfasdf====");
$(document).ready(function(){
  // console.log("asdaflkjalsdkfjlakfasdf-----");
  $('#customnav').on('click', function() {
    var $navMenuCont = $($(this).data('target'));
    // console.log("asdaflkjalsdkfjlak",$(document).find($navMenuCont).find("ul.navbar-nav"));
    // $(document).find($navMenuCont).find("ul.navbar-nav").animate({'widht':'toggle'},200)
    $(document).find($navMenuCont).find("ul.navbar-nav").addClass("open")
  });

  $('#closecustomnav').on('click', function(){
    // console.log("dfalsdfkjalkdf=====",$(document).find("#customnav").data('target'));
    var $navMenuCont = $($(document).find("#customnav").data('target'));
    // $(document).find($navMenuCont).find("ul.navbar-nav").animate({'widht':'toggle'},200)
    $(document).find($navMenuCont).find("ul.navbar-nav").removeClass("open")
  })

})
})

// JavaScript Document

//main slider

$('.carousel').carousel({
  interval: 3000,
  pause: false
})



$(document).ready(function() {

      $("#owl-testmonial").owlCarousel({
        items : 1,
        lazyLoad : true,
        navigation : true,
		pagination : false,
		autoPlay: 3000
      });

    });
	
	
//jQuery(document).ready(function($){
	// browser window scroll (in pixels) after which the "back to top" link is shown
	//var offset = 300,
		//browser window scroll (in pixels) after which the "back to top" link opacity is reduced
		//offset_opacity = 1200,
		//duration of the top scrolling animation (in ms)
		//scroll_top_duration = 700,
		//grab the "back to top" link
		//$back_to_top = $('.cd-top');

	//hide or show the "back to top" link
	//$(window).scroll(function(){
		//( $(this).scrollTop() > offset ) ? $back_to_top.addClass('cd-is-visible') : $back_to_top.removeClass('cd-is-visible cd-fade-out');
		//if( $(this).scrollTop() > offset_opacity ) { 
			//$back_to_top.addClass('cd-fade-out');
		//}
	//});

	//smooth scroll to top
	//$back_to_top.on('click', function(event){
		//event.preventDefault();
		//$('body,html').animate({
			//scrollTop: 0 ,
		 	//}, scroll_top_duration
		//);
	//});

//});

new WOW().init();	

	
	



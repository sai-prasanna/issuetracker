 $(window).load(function() {
      $('.flexslider').flexslider({
      animation: "slide"
      });

    });
      var eventFired = false,
    objectPositionTop = $('#total_tickets').offset().top;

  $(window).on('scroll', function() {

     var currentPosition = $(document).scrollTop();
     if (currentPosition > objectPositionTop && eventFired === false) {
        eventFired = true;
        total_tickets = $("#total_tickets").attr('data-count');
        resolved_tickets = $("#resolved_tickets").attr('data-count');

        var ticketAnim = new countUp("total_tickets", 0,total_tickets,0,2);
        var resolvedAnim = new countUp("resolved_tickets", 0,resolved_tickets,0,2);

        ticketAnim.start();
        resolvedAnim.start();

 }

});
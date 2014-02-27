(function($){
  $(document).ready(function() {

    window.images = new Array();
    window.timers = new Array();

    function preloadImages(arrayOfImages) {
      $('#imgcontainer').remove();
      $('<div id="imgcontainer"></div>').appendTo('body').hide();
      $(arrayOfImages).each(function () {
        $('<img />').attr('src', '/static/images/' + this).appendTo('#imgcontainer').hide();
      });
    }

    function stopTimers() {
      for (var i = 0; i < window.timers.length; i++)
      {
        clearTimeout(window.timers[i]);
      }
    }


    $( '#date' ).change(function () {
      stopTimers();

      var datum = $( this ).val();

      $.ajax({
        url: '/photos/' + datum,
        type: 'get',
        dataType: 'json',
        cache: false,
        success: function(data) {
          data.sort()
          window.images = data;

          $( '#photoslist' ).html('');
          $.each(window.images, function (index, value) {
            $('#photoslist').append('<li><a class="photolink" href="/static/images/' + value + '">' + value + '</a></li>');
          });

          preloadImages(window.images);

          $.each(window.images, function (index, value) {
            timers.push(setTimeout(function() {
              $('#stream').attr('src', "/static/images/" + value);
              $('#actualphoto').html(value);
            }, 200*index));


          });

        },
        async:true
      });



    });

    $('#stop').on('click', function() {
      stopTimers()
    });

    $('#refresh').on('click', function() {
      location.reload();
    });

    $('.photolink').on('click', function(e) {
      e.stopImmediatePropagation();
      e.preventDefault();
      console.log($(this).attr('href'));
      stopTimers();
      $('#stream').attr('src', "/static/images/" + $(this).attr('href'));
      $('#actualphoto').html($(this).attr('href'));
      return false;
    });
  });
})(jQuery);

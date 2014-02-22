(function($){
  $(document).ready(function() {
    $('.graph').each(function () {
      $(this).highcharts({
          chart: {
              type: $(this).data('type')
          },
          title: {
              text: $(this).data('title')
          },
          yAxis: [{
              title: {
                  text: $(this).data('ytitle')
              }
          }
          ],
          xAxis: {
              type: 'datetime'
          },
          series: $(this).data('series')
    });
  });
  });
})(jQuery);

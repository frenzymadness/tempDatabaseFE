(function($){
  $(document).ready(function() {
  Highcharts.setOptions({
    global: {
        timezoneOffset: -1 * 60
            }
    });
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

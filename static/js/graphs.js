(function($){
  $(document).ready(function() {
    Highcharts.setOptions({
      global: {
        timezoneOffset: -1 * 60
      }
    });
    $('.graphline').each(function () {
      $(this).highcharts({
        chart: {
          type: 'line'
        },
        plotOptions: {
          line: {
            marker: {
              enabled: false
            }
          }
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
    $('.graphpie').each(function () {
      $(this).highcharts({
        chart: {
          type: $(this).data('type')
        },
        title: {
          text: $(this).data('title')
        },
        series: [{ type: 'pie',
        data: $(this).data('series') }]
      });
    });
  });
})(jQuery);

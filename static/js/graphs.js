(function($){
  $(document).ready(function() {
    $('.graph').each(function () {
      $(this).highcharts({
          chart: {
              type: 'line'
          },
          title: {
              text: $(this).data('title')
          },
          yAxis: [{
              title: {
                  text: $(this).data('ytitle')
              }
          },{
              title: {
                  text: $(this).data('y2title')
              },
              opposite: true,
              linkedTo: 0,
              tickInterval: 10
          }
          ],
          series: [
          {
              name: 'Tempreature',
              yaxis: 0,
              data: [1, 0, 4,4,4,4,4,4,3,4,3,2,3,4,5,6,5,4,3,4,5,4,3,5,4,3,4]
          },
          {
              name: 'Humidity',
              yaxis: 1,
              data: [10, 10, 40,40,40,40,40,40,30,40,30,20,30,40,50,60,50,40,30,40,50,40,30,50,40,30,40]
          }
          ]
    });
  });
  });
})(jQuery);

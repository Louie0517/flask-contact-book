function dataSet (){
    document.addEventListener("DOMContentLoaded", function () {
    const chartDiv = document.querySelector("#chart");

    const active = JSON.parse(chartDiv.dataset.active)
    const ontime = JSON.parse(chartDiv.dataset.ontime)
    const late = JSON.parse(chartDiv.dataset.late)
    const dates = JSON.parse(chartDiv.dataset.dates)

        var options = {
          series: [{
          name: 'Ontime',
          data: ontime
        }, {
          name: 'Late',
          data: late
        }, {
          name: 'Active',
          data: active
        }],
          chart: {
          type: 'bar',
          height: 350
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '55%',
            borderRadius: 5,
            borderRadiusApplication: 'end'
          },
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          show: true,
          width: 2,
          colors: ['transparent']
        },
        xaxis: {
          categories: dates,
        },
        yaxis: {
          title: {
            text: '$ (thousands)'
          }
        },
        fill: {
          opacity: 1
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return "$ " + val + " thousands"
            }
          }
        }
        };

        var chart = new ApexCharts(document.querySelector("#chart"), options);
        chart.render();
    });
}

dataSet()
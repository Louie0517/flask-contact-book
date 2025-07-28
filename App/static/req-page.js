

function renderRadialChart(selectorId, value) {
  const chartEl = document.getElementById(selectorId);
  const seriesValue = parseFloat(chartEl.dataset.progress) || 0;

  const options = {
    chart: {
      height: 90,
      width: 90,
      type: "radialBar",
      sparkline: { enabled: true }
    },
    series: [seriesValue],
    plotOptions: {
      radialBar: {
        hollow: { size: "60%", 
            margin: 5 
            },
        dataLabels: { show: false,
         },
         track: {
            strokeWidth: '97%',
            margin: 0
         }
      }
    },
    fill: {
        type: 'solid',
        colors: ['#ffc800ff']
    },
  };

  const chart = new ApexCharts(chartEl, options);
  chart.render();
}


function dataChart(){
  document.addEventListener("DOMContentLoaded", function () {
    const chartEl = document.querySelector("#chart");
    const requestData = JSON.parse(chartEl.dataset.requests);

    const options = {
        series: [{
            name: 'Requests',
            data: requestData
        }],
        chart: {
            type: 'area',
            stacked: false,
            height: 350,
            zoom: {
                type: 'x',
                enabled: true,
                autoScaleYaxis: true
            },
            toolbar: {
                autoSelected: 'zoom'
            }
        },
        dataLabels: { enabled: false },
        markers: { size: 0 },
        title: { text: 'Requests Per Day', align: 'left' },
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                inverseColors: false,
                opacityFrom: 0.5,
                opacityTo: 0,
                stops: [0, 90, 100]
            },
        },
        yaxis: {
            labels: {
                formatter: function (val) {
                    return val.toFixed(0);
                },
            },
            title: { text: 'Number of Requests' }
        },
        xaxis: {
            type: 'datetime',
        },
        tooltip: {
            shared: false,
            y: {
                formatter: function (val) {
                    return val.toFixed(0);
                }
            }
        }
    };

    const chart = new ApexCharts(chartEl, options);
    chart.render();
});

}


renderRadialChart("pending-progress", "{{ records.pending }}");
renderRadialChart("approved-progress", "{{ records.approved }}");
renderRadialChart("rejected-progress", "{{ records.rejected }}");
dataChart()
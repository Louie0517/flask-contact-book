function dataset (){
    document.addEventListener("DOMContentLoaded", function () {
    const chartDiv = document.querySelector("#barChart");
    const names = JSON.parse(chartDiv.dataset.names);
    const count = JSON.parse(chartDiv.dataset.count);

    
    var options = {
          series: [{
          name: 'Count of request',
          data: count
        }],
          chart: {
          height: 350,
          type: 'bar',
        },
        plotOptions: {
          bar: {
            borderRadius: 10,
            dataLabels: {
              position: 'top', 
            },
          }
        },
        dataLabels: {
          enabled: true,
          formatter: function (val) {
            return val;
          },
          offsetY: -20,
          style: {
            fontSize: '12px',
            colors: ["#304758"]
          }
        },
        
        xaxis: {
          categories: names,
          position: 'top',
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false
          },
          crosshairs: {
            fill: {
              type: 'gradient',
              gradient: {
                colorFrom: '#D8E3F0',
                colorTo: '#BED1E6',
                stops: [0, 100],
                opacityFrom: 0.4,
                opacityTo: 0.5,
              }
            }
          },
          tooltip: {
            enabled: true,
          }
        },
        yaxis: {
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false,
          },
          labels: {
            show: false,
            formatter: function (val) {
              return val;
            }
          }
        
        },
        title: {
          text: 'Top request employee',
          floating: true,
          offsetY: 330,
          align: 'center',
          style: {
            color: '#444',
          }
        }
        };

        var chart = new ApexCharts(chartDiv, options);
        chart.render();
});

}

function trackRecord(){
  document.addEventListener("DOMContentLoaded", function () {

    const container = document.querySelector("#trackRecord");
    const ontime = parseInt(container.dataset.ontime);
    const late = parseInt(container.dataset.late);
    const active = parseInt(container.dataset.active);


    var options = {
          series: [20, 24, 22],
          chart: {
          width: 380,
          height: 347,
          type: 'polarArea', 
          toolbar: {
            show: true
          }
        },
        labels: ['Ontime', 'Late', 'Active'],
        fill: {
          colors: ['#FF4560', '#ffd000ff', '#a136ffff'],
          opacity: 2
        },
        stroke: {
          width: 0,
          colors: undefined
        },
        yaxis: {
          show: false
        },
        legend: {
          position: 'bottom'
        },
        plotOptions: {
          polarArea: {
            rings: {
              strokeWidth: 0
            },
            spokes: {
              strokeWidth: 0
            },
            dataLabels: {
              position: 'top'
            }
          }
        },
        theme: {
          monochrome: {
            enabled: false
          }
        }
        };

        var chart = new ApexCharts(container, options);
        chart.render();
  });
}

function requestRecord(){
  const track = document.querySelector("#requestTrack");

   var options = {
          series: [{
          name: 'series1',
          data: [31, 40, 28, 51, 42, 109, 100]
        }, {
          name: 'series2',
          data: [11, 32, 45, 32, 34, 52, 41]
        }],
          chart: {
          height: 350,
          type: 'area'
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth'
        },
        xaxis: {
          type: 'datetime',
          categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
        },
        tooltip: {
          x: {
            format: 'dd/MM/yy HH:mm'
          },
        },
        };

        var chart = new ApexCharts(track, options);
        chart.render();
      
}

function totalTracker() {

  const totalId = document.querySelector("#totalTracker");

  var options = {
          series: [
          {
            name: "Low - 2013",
            data: [12, 11, 14, 18, 35, 13, 13]
          }
        ],
          chart: {
          height: 350,
          type: 'line',
          dropShadow: {
            enabled: true,
            color: '#000',
            top: 18,
            left: 7,
            blur: 10,
            opacity: 0.5
          },
          zoom: {
            enabled: false
          },
          toolbar: {
            show: false
          }
        },
        colors: ['#545454'],
        dataLabels: {
          enabled: true,
        },
        stroke: {
          curve: 'smooth'
        },
        title: {
          text: 'Average High & Low Temperature',
          align: 'left'
        },
        grid: {
          borderColor: '#e7e7e7',
          row: {
            colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          },
        },
        markers: {
          size: 1
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
          title: {
            text: 'Month'
          }
        },
        yaxis: {
          title: {
            text: 'Temperature'
          },
          min: 5,
          max: 40
        },
        legend: {
          position: 'top',
          horizontalAlign: 'right',
          floating: true,
          offsetY: -25,
          offsetX: -5
        }
        };

        var chart = new ApexCharts(totalId, options);
        chart.render();
      
}

dataset()
trackRecord()
requestRecord()
totalTracker()
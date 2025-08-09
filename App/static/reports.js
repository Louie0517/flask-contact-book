
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
          offsetY: 60,
          style: {
            fontSize: '19px',
            colors: ["#304758"]
          }
        },
        
        xaxis: {
          categories: names,
          position: 'bottom',
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
          offsetY: -5,
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
          width: 360,
         
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
          name: 'Late',
          data: [31, 40, 28, 51, 42, 109, 100]
        }, {
          name: 'Ontime',
          data: [11, 32, 45, 32, 34, 52, 41]
        }],
          chart: {
          height: 350,
          type: 'area'
        },
        title: {
          text: 'Late vs Ontime',
          align:  'center'
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
            show: true
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
          text: 'Number of Employee',
          align: 'center'
        },
        grid: {
          borderColor: '#e7e7e7',
          row: {
            colors: ['#f3f3f3', 'transparent'], 
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
            text: 'Count'
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

function infoLineGraph(elementId, seriesName){

  const now = new Date();
  let dates = [];
  let baseValue = 1000000;
  for (let i = 0; i < 20; i++) {
    dates.push([now.getTime() + i * 86400000, baseValue + Math.floor(Math.random() * 500000)]);
  }

  var options = {
    series: [{
      name: seriesName,
      data: dates
    }],
    chart: {
      type: 'area',
      stacked: false,
      height: 150,
      sparkline: {
        enabled: true
      },
      zoom: {
        type: 'x',
        enabled: true,
        autoScaleYaxis: true
      },
      toolbar: {
        autoSelected: 'zoom'
      }
    },
    dataLabels: {
      enabled: false
    },
    markers: {
      size: 0
    },
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        inverseColors: false,
        opacityFrom: 0.5,
        opacityTo: 0,
        stops: [0, 90, 100]
      }
    },
    yaxis: {
      labels: {
        formatter: function (val) {
          return (val / 1000000).toFixed(1);
        }
      }
    },
    xaxis: {
      type: 'datetime'
    },
    tooltip: {
      shared: false,
      y: {
        formatter: function (val) {
          return (val / 1000000).toFixed(2) ;
        }
      }
    }
  };
  
  var activateChart = new ApexCharts(document.querySelector(elementId), options);
  
  activateChart.render()
}

function date(){
  const today = new Date();
  const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const stringDay = days[today.getDay()];
  const format = stringDay;
  const dates = today.getDate().toString().padStart(2, '0') + '-' +
  (today.getMonth() + 1).toString().padStart(2, '0') + '-' + today.getFullYear();

  document.getElementById("day").textContent = format;
  document.getElementById("date").textContent = dates
}

dataset()
trackRecord()
requestRecord()
totalTracker()
infoLineGraph('#pr-3', 'Late Employee')
infoLineGraph('#pr-1', 'Total Employee')
infoLineGraph('#pr-2', 'Ontime Employee')
date()


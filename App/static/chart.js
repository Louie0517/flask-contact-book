function lineGraph() {
  document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('deptChart'); 
    const labels = JSON.parse(canvas.dataset.labels);
    const data = JSON.parse(canvas.dataset.counts);

    var options = {
      series: data,
      labels: labels,
      chart: {
        width: 500,
        type: 'donut',
        animations: {
            enabled: true
        }
      },
      plotOptions: {
        pie: {
          startAngle: -90,
          endAngle: 270,
          pie: {
            dataLabels: {
                style: {
                    fontSize: '20px'
                }
            }
          }
        }
      },
      dataLabels: {
        style: {
            fontSize: '13px'
        }
      },
      fill: {
        type: 'gradient',
      },
      legend: {
        formatter: function(val, opts) {
          return val + " - " + opts.w.globals.series[opts.seriesIndex];
        }
      },
      title: {
        text: 'Employees per Department'
      },
      responsive: [{
        breakpoint: 480,
        options: {
          chart: {
            width: 200
          },
          legend: {
            position: 'bottom'
          }
        }
      }]
    };

    const chart = new ApexCharts(document.querySelector("#deptChart"), options); // match ID
    chart.render();
  });
}


function mixChart() {

  document.addEventListener("DOMContentLoaded", function () {
    const canvas = document.getElementById("mixChart");

    

    const ontime = JSON.parse(canvas.dataset.ontime);      
    const late = JSON.parse(canvas.dataset.late);          
    const active = JSON.parse(canvas.dataset.active);      

    const data = {
        labels: ['Ontime', 'Late', 'Active'],
        datasets: [{
            label: 'Attendance Stats',
            data: [ontime, late, active],
            backgroundColor: ['rgba(86, 206, 239, 1)', 'rgba(88, 196, 226, 1)', 'rgba(40, 179, 218, 1)'], 
            borderColor: ['rgba(99, 102, 241, 0.7)', 'rgba(239, 68, 68, 0.7)', 'rgba(34, 197, 94, 0.7)'],
            borderWidth: 0,
        }]
    };

    const config = {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            plugins: {
                legend: {
                    display: true
                },
                tooltip: {
                    enabled: true
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                }
            }
        }
    };

    new Chart(canvas, config);
});

}

function hideSideBar(){
    window.addEventListener('resize', function () {
    const offcanvas = document.getElementById('sidebarOffcanvas');
    const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvas);

    if (window.innerWidth >= 801 && bsOffcanvas) {
      bsOffcanvas.hide();

    const backdrop = document.querySelector('.offcanvas-backdrop');
    if (backdrop) backdrop.remove();
    }
  });
}

lineGraph()
hideSideBar()
mixChart()
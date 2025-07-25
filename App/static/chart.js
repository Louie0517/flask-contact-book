
function lineGraph(){
document.addEventListener("DOMContentLoaded", () => {
    const canvas = document.getElementById('deptChart');
    const labels = JSON.parse(canvas.dataset.labels);
    const data = JSON.parse(canvas.dataset.counts);

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Employees per Department',
                data: data,
                borderColor: 'rgba(40, 179, 218, 1)',
                backgroundColor: 'rgba(46, 226, 236, 0.5)',
                fill: true,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Employees by Department'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
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


mixChart()
lineGraph()

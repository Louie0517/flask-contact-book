function averageAttendance (){
    const chartID = document.getElementById("chart");
    const averageLabel = parseFloat(chartID.dataset.attendance);
    const year = averageLabel.year;
    const average = averageLabel.average;

    const options = {
        chart: {
            type: 'bar'
        },
        series: [{
            name: 'Average Attendance Hours',
            data: average
        }],
        xaxis: {
            categories: year
        }
    };

    const chart = new ApexCharts(document.querySelector("#attendanceChart"), options);
    chart.render();
    
}

averageAttendance()
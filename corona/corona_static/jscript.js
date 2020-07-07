    $(function () {
      var $pieChart = $("#pie-chart");
      $.ajax({
        url: $pieChart.data("url"),
        success: function (data) {
          var ctx = $pieChart[0].getContext("2d");
          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Patient Count',
                backgroundColor: [
                '#ffffff', '#ffffff', '#ffffff', '#ffffff', '#ffffff', '#ffe6e6', '#ffe6e6', '#ffe6e6',
                '#ffe6e6', '#ffe6e6', '#ffcccc', '#ffcccc', '#ffcccc', '#ffcccc', '#ffcccc', '#ffb3b3',
                '#ffb3b3', '#ffb3b3', '#ffb3b3', '#ffb3b3', '#ff9999', '#ff8080', '#ff6666', '#ff4d4d',
                '#ff3333', '#ff1a1a', '#ff0000', '#e60000', '#cc0000', '#b30000', '#990000', '#800000',
                '#660000', '#4d0000', '#330000', '#1a0000', '#000000'
                ],
                data: data.data
              }]
            },
            options: {
              responsive: true,
              legend: {
                position: 'left',
                labels: {
                fontSize: 14,
                fontColor: 'rgb(0, 0, 0)'
            }
              },
              title: {
                position: 'left',
                display: true,
                text: 'Corona Active Patients Across India Statistics Pie Chart',
                fontColor: 'rgb(0, 0, 0)',
                fontSize: 18,
              }
            }
          });
        }
      });
    });

$(function () {
      var $populationChart = $("#population-chart");
      $.ajax({
        url: $populationChart.data("url"),
        success: function (data) {
          var ctx = $populationChart[0].getContext("2d");
          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Active Patients',
                backgroundColor: '#C0392B',
                data: data.data
              }]
            },
            options: {
              responsive: true,
              scales: {
              yAxes: [{
              ticks: {fontColor: "black", fontSize: 15},
              }],
              xAxes: [{
              ticks: {fontColor: "black", fontSize: 15}
              }]
              },
              legend: {
                position: 'top',
                labels: {
                fontSize: 18,
                fontColor: 'rgb(0, 0, 0)'
            }
              },
              title: {
                position: 'left',
                display: true,
                text: 'Corona Active Patient Statistics Bar Graph',
                fontColor: 'rgb(0, 0, 0)',
                fontSize: 18,
              }
            }
          });
        }
      });
    });

$(function () {
      var $populationChart = $("#line-chart");
      $.ajax({
        url: $populationChart.data("url"),
        success: function (data) {
          var ctx = $populationChart[0].getContext("2d");
          new Chart(ctx, {
            type: 'line',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Confirmed',
                data: data.total_confirmed,
                fill: false,
                borderColor: 'red',
                lineJoin: 'round'
              },
              {
                label: 'Recovered',
                data: data.total_recovered,
                fill: false,
                borderColor: 'green',
                lineJoin: 'round'
              },
              {
                label: 'Death',
                data: data.total_death,
                fill: false,
                borderColor: 'black',
                lineJoin: 'round'
              }
              ]
            },
            options: {
              responsive: true,
              scales: {
              yAxes: [{
              ticks: {fontColor: "black", fontSize: 15},
              }],
              xAxes: [{
              ticks: {fontColor: "black", fontSize: 15}
              }]
              },
              legend: {
                position: 'top',
                labels: {
                fontSize: 18,
                fontColor: 'rgb(0, 0, 0)'
            }
              },
              title: {
                position: 'left',
                display: true,
                text: 'Corona Patient Across India Statistics Date wise line chart',
                fontColor: 'rgb(0, 0, 0)',
                fontSize: 18,
              }
            }
          });
        }
      });
    });
// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var ctx = document.getElementById("MostExecuted");
var MostExecuted = new Chart(ctx, {
  type: 'doughnut',
  data: {
    datasets: [{
      label: "Sessions",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [],
    }],
    labels: [],
  },
});


$(document).ready(function () {
  $.ajax({
    url: "/MostExecuted",
    type: "GET",
    success: function (data) 
    {

      MostExecuted.data.labels = data.labels;
      MostExecuted.data.datasets[0].data = data.values;
      MostExecuted.update();

    }
  });
});

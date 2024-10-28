// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var ctx = document.getElementById("perMonth");
var perMonth = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ["Janeiro", "Fevereiro", "Março", "Abril", 
      "Maio", "Junho", "Julho", "Agosto", 
      "Setembro", "Outubro", "Novembro", "Dezembro"],

    datasets: [{
      label: "Execuções",
      backgroundColor: "rgba(2,117,216,1)",
      borderColor: "rgba(2,117,216,1)",
      data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }],
  },

});


$(document).ready(function () {
  $.ajax({
    url: "/PerMonth",
    type: "GET",
    success: function (data) {

      perMonth.data.labels.forEach((item, pos) => {
        
        var pos = parseInt(pos);
        for (label of data.labels){

          if (perMonth.data.labels[pos].toLowerCase() === label.toLowerCase())
          {
            perMonth.data.datasets[0].data[pos] = data.values[pos];
            break
          }
        }

        
      });
      perMonth.update();

    }
  });
});

// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var ctx = document.getElementById("MostExecuted");
var MostExecuted = new Chart(ctx, {
  type: 'doughnut',
  data: {
    datasets: [{
      label: "Execuções",
      lineTension: 0.3,
      backgroundColor: [
        "#FF9800", "#FF5722", "#795548", "#9E9E9E", "#607D8B", "#F44336", "#E57373", "#BA68C8",
        "#8D6E63", "#D84315", "#A1887F", "#4E342E", "#3E2723", "#D32F2F", "#FFA726", "#EF6C00",
        "#BCAAA4", "#A1887F", "#8E24AA", "#5D4037", "#7B1FA2", "#8E8E8E", "#6D4C41", "#FF7043",
        "#FF8A65", "#6A1B9A", "#FFAB91", "#F57F17", "#B39DDB", "#9C27B0", "#E65100", "#6A1B9A",
        "#D4E157", "#9C9C9C", "#BF360C", "#FFCCBC", "#616161", "#BDBDBD", "#8D6E63", "#C62828"
    ],
      borderColor: [
        "#CC7A00", "#CC471A", "#5D4037", "#7E7E7E", "#4A5C6B", "#CC3726", "#CC4F4F", "#9546A8",
        "#715A54", "#AB3413", "#826F66", "#3D2E2A", "#31211F", "#B72B29", "#E48920", "#CB5C00",
        "#9A7D73", "#826F66", "#7A1D90", "#4C3B34", "#681C85", "#737373", "#583F37", "#CC5C37",
        "#CC7557", "#581682", "#CC9171", "#C26D14", "#977BB8", "#811B92", "#B34700", "#581682",
        "#A4BD41", "#808080", "#99310B", "#CCAC9C", "#494949", "#989898", "#715A54", "#A32222"
      ],
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [0.1, 0.1, 0.1],
    }],
    labels: ["Carregando", "Carregando", "Carregando"],
  },
});


$(document).ready(function () {
  $.ajax({
    url: "/MostExecuted",
    type: "GET",
    success: function (data) {

      MostExecuted.data.labels = data.labels;
      MostExecuted.data.datasets[0].data = data.values;
      MostExecuted.update();

    }
  });
});

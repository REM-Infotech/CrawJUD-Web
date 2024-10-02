// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

document.addEventListener('DOMContentLoaded', function () {

    var pid = document.documentElement.dataset.pid;
    var total_rows = this.documentElement.dataset.total_rows;

    var ul = document.getElementById('messages'); // Elemento <ul> onde as mensagens de log são exibidas
    var percent_progress = document.getElementById('progress_info');

    var ctx = document.getElementById("LogsBotChart");
    var LogsBotChart = new Chart(ctx, {
        type: 'pie',
        data: {
        labels: ["TOTAL", "SUCESSOS", "ERROS"],
        datasets: [{
            data: [total_rows, 0, 0],
            backgroundColor: ['#d3e3f5', '#42cf06', "#FF0000"],
        }],
        },
    });

    fetch(`/socket_address/${pid}`)
        .then(response => response.text())
        .then(socketAddress => {

            var socket = io.connect(socketAddress + '/log');
            socket.on('connect', function () {
                socket.emit('join', { 'pid': pid });
            });
            socket.on('disconnect', function () {
                socket.emit('leave', { 'pid': pid });
            });

            socket.on('log_message', function (data) {
                var messagePid = data.pid;
                var pos = parseInt(data.pos);
                var typeLog = data.type;
                var value_error = LogsBotChart.data.datasets[0].data[2];
                var value_success = LogsBotChart.data.datasets[0].data[1];
                if (messagePid === pid) {

                    var msg = data.message;
                    var li = document.createElement('li');

                    li.style.fontWeight = "bold";
                    li.style.color = '#d3e3f5';

                    if (typeLog === "error") {

                        li.style.fontWeight = "bold";
                        li.style.color = 'RED';
                        LogsBotChart.data.datasets[0].data[2] += 1;
                        LogsBotChart.data.datasets[0].data[0] -= 1;

                        if (pos === 0){
                            LogsBotChart.data.datasets[0].data[0] = 0;
                            LogsBotChart.data.datasets[0].data[2] = total_rows;
                        };

                    } else if (typeLog === "success") {

                        value_success = value_success + 1
                        LogsBotChart.data.datasets[0].data[1] += 1;
                        li.style.color = '#42cf06';
                        li.style.fontWeight = "bold";
                        LogsBotChart.data.datasets[0].data[0] -= 1;

                    };
                    
                    LogsBotChart.update();
                    li.appendChild(document.createTextNode(msg));
                    ul.appendChild(li);

                    var randomId = "id_" + pos + pid;

                    li.setAttribute("id", randomId);
                    document.getElementById(randomId).scrollIntoView({ behavior: "smooth", block: "end" });

                    var total_rows_subtract = total_rows - 1;
                    var progress = (pid / total_rows_subtract) * 100;
                    var textNode = document.createTextNode(progress.toFixed(2) + '%');

                    if (pos !== 0) {
                        var subtrac = pos - 1;
                        var progress = (subtrac / total_rows_subtract) * 100;
                        var textNode = document.createTextNode(progress.toFixed(2) + '%');

                    }
                    percent_progress.innerHTML = '';
                    percent_progress.appendChild(textNode);
                    percent_progress.style.width = progress + '%';

                    // if (data.labels.length > 0){
                    //     LogsBotChart.data.labels = data.labels;
                    //   };
              
                    //   if (data.values.length > 0){
                    //     LogsBotChart.data.datasets[0].data = data.values;
                    //   };
              
                    //   if (data.labels.length > 0 && data.values.length > 0){
                    //     LogsBotChart.update();
                    //   }
                }
            });
        });
    // Função para extrair o número da posição da mensagem de log
    function checkStatus() {
        fetch(`/status/${pid}`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
            })
            .then(data => {
                if (data && data.document_url) {
                    const downloadButton = document.getElementById('download-button');
                    downloadButton.href = data.document_url;
                    downloadButton.classList.remove('disabled');
                    downloadButton.classList.remove('btn-outline-success');
                    downloadButton.classList.add('btn-success');
                    downloadButton.setAttribute('aria-disabled', 'false');
                } else {
                    console.warn('Invalid data:', data);
                }
            })
            .catch(error => {
                console.error('Erro de rede:', error);
            });
    }

    setInterval(checkStatus, 15000);
    checkStatus(pid);
})


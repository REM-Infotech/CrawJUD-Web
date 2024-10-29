window.addEventListener('DOMContentLoaded', event => {

    var datatablesSimple = document.querySelector(
        'table[id="DataTable"]');
    if (datatablesSimple) {
        new DataTable(datatablesSimple,{

            searching: false,
            deferRender: true,
            deferLoading: 57,
            processing: true
            

        });
    };
});

$(document).ready(function() {

    var location_url = $(location).attr('href');
    console.log(location_url);

    if (location_url.toLowerCase().includes("dashboard") || location_url.toLowerCase().includes("executions")){
        var targets = [4, 6];
    } else if(location_url.toLowerCase().includes("users")){
        var targets = [4];
    };

    $('#FormatedDataTable').DataTable({  
        columnDefs: [
            {
                targets: targets,
                render: DataTable.render.datetime('D/MMM/YYYY', "pt")
            }
        ]
    });
});

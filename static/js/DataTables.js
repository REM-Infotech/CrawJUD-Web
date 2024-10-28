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

    $('#DashDataTable').DataTable({  
        columnDefs: [
            {
                targets: [4, 6],
                render: DataTable.render.datetime('D/MMM/YYYY', "pt")
            }
        ]
    });
});

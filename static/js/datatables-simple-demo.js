window.addEventListener('DOMContentLoaded', event => {

    var datatablesSimple = document.querySelector(
        'table');
    if (datatablesSimple) {
        new DataTable(datatablesSimple,{

            deferRender: true,
            deferLoading: 57,
            processing: true
            

        });
    };
});
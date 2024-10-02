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
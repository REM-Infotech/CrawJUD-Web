var ModalMessage = document.getElementById('ModalMessage');
if (ModalMessage != null) {
    $(document).ready(function () {
        $('#ModalMessage').modal('show');
    });
}


window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});

// Função para filtrar os cards
function filterCards(element) {
    // Pegar o valor digitado no campo de busca
    var input = element;
    var filter = input.value.toUpperCase();

    // Pegar todos os cards
    var cards = document.getElementsByClassName('col-md-3');
    // Loop através dos cards e esconder aqueles que não correspondem à pesquisa
    for (var i = 0; i < cards.length; i++) {
        var title = cards[i].getElementsByClassName('card-header')[0];
        if (title) {
            var titleText = title.textContent || title.innerText;
            if (titleText.toUpperCase().indexOf(filter) > -1) {
                cards[i].style.display = '';
            } else {
                cards[i].style.display = 'none';
            }
        }
    }
}
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

var selectors = document.getElementsByTagName("select");

if (selectors.length > 0) {
  for (let element of selectors) {  // Mudança aqui, para usar 'for...of' em vez de 'for...in'

    $(document).ready(function () {
      // Aqui podemos usar jQuery diretamente, pois estamos aplicando ao próprio elemento
      $(element).select2({
        theme: "bootstrap-5",
        width: $(element).data('width') ? $(element).data('width') : $(element).hasClass('w-100') ? '100%' : 'style',
        placeholder: $(element).data('placeholder'),
      });
    });
  }
}

function authMethodChange(element) {

    let div_cert = document.querySelector('div[id="cert"]');
    let div_pw = document.querySelector('div[id="pw"]');

    if (element.value === "cert"){
        div_cert.style.display = "block";
        div_pw.style.display = "none";

    } else if (element.value === "pw"){
        div_cert.style.display = "none";
        div_pw.style.display = "block";
    }
}

function showLoad(){
    setTimeout(() => {
        $('#modalLoading').modal('show');
    }, 500)
}


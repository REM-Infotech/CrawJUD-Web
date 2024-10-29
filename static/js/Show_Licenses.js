$(document).ready(function () {

    var TipoUser = $("select[id='tipo_user']");
    var DivLicenses = $("div[id='licenses']");
    var licensesOptions = $("select[id='licenses']");

    // Armazena a primeira opção
    var optionFirst = licensesOptions.find('option:first');

    var lastOption = optionFirst.clone(); // Clona a primeira opção
    var lastOptionValue = optionFirst.val(); // Armazena o valor da primeira opção

    DivLicenses.attr("style", "");
    licensesOptions.find('option:first').remove();

    TipoUser.change(function () {

        if (TipoUser.val() === "admin") {

            // Remove a primeira opção apenas se ela for igual a lastOption
            if (licensesOptions.find('option:first').val() === lastOptionValue &&
                TipoUser.val() !== "default_user") {
                licensesOptions.find('option:first').remove();
            }
            DivLicenses.attr("style", "");

            // Atualiza o Select2 para refletir a alteração
            licensesOptions.trigger('change.select2');

        } else if (TipoUser.val() === "supersu" || TipoUser.val() === "default_user") {

            DivLicenses.attr("style", "");
            if (TipoUser.val() !== "default_user"){
                DivLicenses.attr("style", "display: none;");
            }
            
            // Adiciona novamente a opção se ela não estiver presente
            if (licensesOptions.find(`option[value="${lastOptionValue}"]`).length === 0) {
                licensesOptions.prepend(lastOption);
                licensesOptions.trigger('change.select2'); // Atualiza o Select2
            }
        }

        // Limpar a seleção atual
        licensesOptions.val(null).trigger('change');
    });
});

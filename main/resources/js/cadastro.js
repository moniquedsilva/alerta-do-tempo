window.addEventListener("load", function () {
    //Carrega DropDown de Munícipio assim que carrega a página
    populaMuncipio();

    //Eventos
    //Submit do formulário
    document
        .getElementById("form_cadastro")
        .addEventListener("submit", submitForm);
    //OnChange do Estado
    document
        .getElementById("estado")
        .addEventListener("change", populaMuncipio);

    let tokens = document.getElementsByName("csrfmiddlewaretoken");
    let csrf_token = tokens[0].getAttribute("value");

    //Submit do formulário
    function submitForm(event) {
        event.preventDefault();

        let xhr = new XMLHttpRequest();
        var url = URL_SUBMIT_FORM;

        xhr.open("POST", url, true);
        xhr.setRequestHeader("Accept", "application/x-www-form-urlencoded");
        xhr.setRequestHeader(
            "Content-Type",
            "application/x-www-form-urlencoded"
        );
        xhr.setRequestHeader("X-CSRF-Token", csrf_token);

        xhr.onload = () => respostaSubmitForm(xhr.responseText);
        let data = new URLSearchParams(new FormData(event.target)).toString();
        xhr.send(data);
    }

    //Resposta para inserção do cadastro
    function respostaSubmitForm(respostaJSON) {
        var resposta = JSON.parse(respostaJSON);
        if (resposta["status"] == true) {
            document.getElementById("form_cadastro").reset();
        }
        alert(resposta["msg"]);
    }

    function populaMuncipio() {
        let xhr = new XMLHttpRequest();
        var url = URL_LOAD_MUNICIPIOS;
        console.log(url);

        xhr.open("POST", url, true);
        xhr.setRequestHeader("Accept", "application/json");
        xhr.setRequestHeader("Content-Type", "application/json");

        xhr.onload = () => respostaPopulaMunicipio(xhr.response);
        let dados = { estado_id: document.getElementById("estado").value };
        let data = JSON.stringify(dados);
        xhr.send(data);
    }

    function respostaPopulaMunicipio(dadosJSON) {
        var dados = JSON.parse(dadosJSON);
        let select = document.getElementById("municipio");
        select.innerHTML = "";
        for (d of dados["municipios"]) {
            var opt = document.createElement("option");
            for (key in d) {
                opt.value = key;
                opt.innerHTML = d[key];
                select.appendChild(opt);
            }
        }
    }
});

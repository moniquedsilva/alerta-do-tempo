window.addEventListener("load", function () {
    //Token csrf
    let tokens = document.getElementsByName("csrfmiddlewaretoken");
    let csrf_token = tokens[0].getAttribute("value");

    //Eventos
    //Submit do formulário
    document
        .getElementById("form_login")
        .addEventListener("submit", submitForm);

    //Submit do formulário
    function submitForm(event) {
        event.preventDefault();

        let xhr = new XMLHttpRequest();
        let url = URL_SUBMIT_FORM;

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

    //Resposta para tentativa de login
    function respostaSubmitForm(respostaJSON) {
        let resposta = JSON.parse(respostaJSON);

        if (!resposta["status"]) {
            //login falhou
            let alerta = document.getElementById("alerta");
            alerta.textContent = resposta["msg"];
            let kf_alerta_slide = [
                { top: "-15vh" },
                { top: "0", offset: 0.15 },
                { top: "0", offset: 0.85 },
                { top: "-15vh", visibility: "visible" },
            ];
            let options = { easing: "ease", duration: 7000, fill: "backwards" };
            alerta.animate(kf_alerta_slide, options);
        } else {
            //login com sucesso
            window.location.replace(URL_REDIRECT);
        }
    }
});

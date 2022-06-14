window.addEventListener("load", function () {
    //Token csrf
    let tokens = document.getElementsByName("csrfmiddlewaretoken");
    let csrf_token = tokens[0].getAttribute("value");
    
    carregaDados();

    function carregaDados(){

        let xhr = new XMLHttpRequest();
        let url = URL_PREVISAO;
    
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Accept", "application/x-www-form-urlencoded");
        xhr.setRequestHeader(
            "Content-Type",
            "application/x-www-form-urlencoded"
        );
        let formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrf_token);
        xhr.onloadstart = () => carregandoDados();
        xhr.onload = () => respostaDados(xhr.response);
        let data = new URLSearchParams(formData).toString();
        xhr.send(data);
    
    }

    function carregandoDados(){
        //animação loading
    }
    
    function respostaDados(dadosJSON){
        let dados = JSON.parse(dadosJSON);
        // Carrega dados
        // Desativa animação loading
        
        console.log(dados);
    }
});


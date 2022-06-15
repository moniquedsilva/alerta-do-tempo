window.addEventListener("load", function () {
    //Token csrf
    let tokens = document.getElementsByName("csrfmiddlewaretoken");
    let csrf_token = tokens[0].getAttribute("value");

    carregaDados();

    function carregaDados() {
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

    function carregandoDados() {
        //animação loading
    }

    function formatarData(data) {
        const [yyyy, mm, dd] = data.split("-");
        return `${dd}/${mm}/${yyyy}`;
    }

    function respostaDados(dadosJSON) {
        let main = document.getElementById("alerts");
        let dados = JSON.parse(dadosJSON);
        const { chuvas_iuv, ondas } = dados;
        chuvas_iuv.lista_previsao.forEach((item) => {
            const dia = formatarData(item.dia);
            let alerta = `
                <div class="dashboard__alerts-conteudo">
                    <h2>${dia} </h2>
                    <div class="dashboard__alerts-temperatura">
                        <h3>Máxima: ${item.maxima}</h3>
                        <h3>Mínima: ${item.minima}</h3>
                    </div>
                    <p class="dashboard__alerts-tipo">${item.tempo_descricao}</p>
                </div>
            `;

            main.innerHTML += alerta;
        });
        console.log(chuvas_iuv.lista_previsao);
    }
});

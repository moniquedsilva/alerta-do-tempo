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
        let main = document.getElementById("alerts");
        const loading = `
            <div class="loader">
                <div class="loader-wheel"></div>
                <div class="loader-text"></div>
            </div>
        `;
        main.innerHTML += loading;
    }

    function formatarData(data) {
        const [yyyy, mm, dd] = data.split("-");
        return `${dd}/${mm}/${yyyy}`;
    }

    function climaIcon(tipo) {
        if (
            tipo === "ci" ||
            tipo === "c" ||
            tipo === "ch" ||
            tipo === "pp" ||
            tipo === "pc"
        )
            return "chuvoso";
        else if (tipo === "np" || tipo === "pn" || tipo === "n" || tipo === "e")
            return "nublado";
        else if (tipo === "t") return "tempestade";
        else if (tipo === "ps" || tipo === "cl") return "ensolarado";
        else if (tipo === "g" || tipo === "ne") return "nevada";
        else {
            return "parcialmente-nublado";
        }
    }

    function respostaDados(dadosJSON) {
        let main = document.getElementById("alerts");
        main.innerHTML = "";
        let dados = JSON.parse(dadosJSON);
        const { chuvas_iuv } = dados;
        chuvas_iuv.lista_previsao.forEach((item) => {
            const dia = formatarData(item.dia);
            const icon = climaIcon(item.tempo);
            let alerta = `
                <div class="dashboard__alerts-conteudo">
                    <div class="dashboard__alerts-texto">
                        <h2>${dia}</h2>
                        <div class="dashboard__alerts-temperatura">
                            <h3>Máxima: ${item.maxima}</h3>
                            <h3>Mínima: ${item.minima}</h3>
                        </div>
                        <p class="dashboard__alerts-tipo">${item.tempo_descricao}</p>
                    </div>
                    <img src="/main/resources/assets/images/${icon}.png" alt="${item.tempo}-tempo" class="dashboard__alerts-img" />
                </div>
            `;

            main.innerHTML += alerta;
        });
        console.log(chuvas_iuv.lista_previsao);
    }
});

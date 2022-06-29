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
        let main = document.getElementById("alerta");
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

    function respostaDados(dadosJSON) {
        let dados = JSON.parse(dadosJSON);
        const { chuvas_iuv, usuario } = dados;

        let titulo = document.getElementById("titulo");
        titulo.innerText = `Índice UV`;

        let fraseInicio = document.getElementById("texto");
        fraseInicio.innerText = `Previsão do índice UV para os próximos 4 dias em ${usuario.municipio}, ${usuario.estado}.`;

        let main = document.getElementById("alerta");
        main.innerHTML = "";
        for (let i = 0; i < 4; i++) {
            const item = chuvas_iuv.lista_previsao[i];
            const dia = formatarData(item.dia);
            let previsaoUV = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>${dia}</h2>
                        <div class="alertas-temperatura">
                            <p>${item.iuv}</p>
                        </div>
                        <p class="alertas-tipo">${item.iuv_descricao}</p>
                    </div>
                    <img src="/main/resources/assets/images/ensolarado.png" alt="ensolarado" class="alertas-img" />
                </div>
            `;

            main.innerHTML += previsaoUV;
        }
    }
});

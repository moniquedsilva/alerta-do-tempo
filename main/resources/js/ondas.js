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
        const separarData = data.split(" ");
        const [dd, mm, yyyy] = separarData[0].split("-");
        return `${dd}/${mm}/${yyyy}`;
    }

    function respostaDados(dadosJSON) {
        let dados = JSON.parse(dadosJSON);
        const { ondas, usuario } = dados;

        let titulo = document.getElementById("titulo");
        titulo.innerText = `Ondas`;

        let fraseInicio = document.getElementById("texto");
        fraseInicio.innerText = `Previsão da maré para os próximos 4 dias em ${usuario.municipio}, ${usuario.estado}.`;

        let main = document.getElementById("alerta");
        main.innerHTML = "";
        for (let i = 0; i < 4; i++) {
            const item = ondas.lista_previsao[i];
            const dia = formatarData(item.dia);
            let previsaoOndas = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>${dia}</h2>
                        <div class="alertas-temperatura">
                            <p>Altura: ${item.altura} m</p>
                        </div>
                        <p class="alertas-tipo">${item.agitacao}</p>
                    </div>
                    <img src="/main/resources/assets/images/ondas.svg" alt="Ondas" class="alertas-img-ondas" />
                </div>
            `;

            main.innerHTML += previsaoOndas;
        }
    }
});

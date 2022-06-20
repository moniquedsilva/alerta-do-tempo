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
        let nomeUsuario = usuario.nome.split(" ");
        titulo.innerText = `Bem vindo(a) ${nomeUsuario[0]}`;

        let fraseInicio = document.getElementById("texto");
        fraseInicio.innerText = `Previsão do tempo para os próximos 4 dias em ${usuario.municipio}, ${usuario.estado}.`;

        let main = document.getElementById("alerta");
        main.innerHTML = "";

        chuvas_iuv.lista_previsao.forEach((item) => {
            const dia = formatarData(item.dia);
            const icon = item.categoria;
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
        console.log(dados);
        /*As categorias do tempo são 6:
        nevada, tempestade, chuvoso, nublado
        parcialmente-nublado e ensolarado*/
    }
});

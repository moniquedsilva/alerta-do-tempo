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

    let main = document.getElementById("alerta");
    main.innerHTML = "";

    let titulo = document.getElementById("titulo");
    titulo.innerText = `índice UV`;

    let fraseInicio = document.getElementById("texto");
    fraseInicio.innerText = `Previsão do índice UV para os próximos 4 dias em Salvador, Bahia.`;

    let previsaoUV = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>28/06/2022</h2>
                        <div class="alertas-temperatura">
                            <p>8.0</p>
                        </div>
                        <p class="alertas-tipo">Muito alto</p>
                    </div>
                    <img src="/main/resources/assets/images/ensolarado.png" alt="ensolarado" class="alertas-img" />
                </div>
            `;

    main.innerHTML += previsaoUV;

    previsaoUV = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>29/06/2022</h2>
                        <div class="alertas-temperatura">
                            <p>8.0</p>
                        </div>
                        <p class="alertas-tipo">Muito alto</p>
                    </div>
                    <img src="/main/resources/assets/images/ensolarado.png" alt="ensolarado" class="alertas-img" />
                </div>
            `;

    main.innerHTML += previsaoUV;

    previsaoUV = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>30/06/2022</h2>
                        <div class="alertas-temperatura">
                            <p>8.0</p>
                        </div>
                        <p class="alertas-tipo">Muito alto</p>
                    </div>
                    <img src="/main/resources/assets/images/ensolarado.png" alt="ensolarado" class="alertas-img" />
                </div>
            `;

    main.innerHTML += previsaoUV;

    previsaoUV = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>01/07/2022</h2>
                        <div class="alertas-temperatura">
                            <p>9.0</p>
                        </div>
                        <p class="alertas-tipo">Muito alto</p>
                    </div>
                    <img src="/main/resources/assets/images/ensolarado.png" alt="ensolarado" class="alertas-img" />
                </div>
            `;

    main.innerHTML += previsaoUV;

    function respostaDados(dadosJSON) {
        console.log(dadosJSON);
    }
});

/*
    function formatarData(data) {
        const [yyyy, mm, dd] = data.split("-");
        return `${dd}/${mm}/${yyyy}`;
    }

    function respostaDados(dadosJSON) {
        let dados = JSON.parse(dadosJSON);
        const { chuvas_iuv } = dados;

        let titulo = document.getElementById("titulo");
        titulo.innerText = `Clima`;

        let fraseInicio = document.getElementById("texto");
        fraseInicio.innerText = `Previsão do tempo para os próximos 4 dias em ${usuario.municipio}, ${usuario.estado}.`;

        let main = document.getElementById("alerta");
        main.innerHTML = "";

        chuvas_iuv.lista_previsao.forEach((item) => {
            const dia = formatarData(item.dia);
            const icon = item.categoria;
            let alerta = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>${dia}</h2>
                        <div class="alertas-temperatura">
                            <p>Máxima: ${item.maxima} ºC</p>
                            <p>Mínima: ${item.minima} ºC</p>
                        </div>
                        <p class="alertas-tipo">${item.tempo_descricao}</p>
                    </div>
                    <img src="/main/resources/assets/images/${icon}.png" alt="${item.tempo}-tempo" class="alertas-img" />
                </div>
            `;
        });
    }
*/

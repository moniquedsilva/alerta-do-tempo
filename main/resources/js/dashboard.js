window.addEventListener("load", function () {
    //Data
    const hoje = new Date();
    const dia = hoje.getDate();
    const mes = hoje.toLocaleString("pt-br", { month: "long" });
    const ano = hoje.getFullYear();
    document.querySelector(".data").innerHTML = `
        <div class="data-dia">${dia}</div>
        <div>
            <div class="data-mes">${mes}</div>
            <div class="data-ano">${ano}</div>
        </div>
    `;

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

    function respostaDados(dadosJSON) {
        let dados = JSON.parse(dadosJSON);
        const { chuvas_iuv, ondas, usuario } = dados;

        let titulo = document.getElementById("titulo");
        let nomeUsuario = usuario.nome.split(" ");
        titulo.innerText = `Bem vindo(a) ${nomeUsuario[0]}`;

        let fraseInicio = document.getElementById("texto");
        fraseInicio.innerText = `Previsão do tempo para ${
            dia + 1
        } de ${mes} em ${usuario.municipio}, ${usuario.estado}.`;

        let main = document.getElementById("alerta");
        main.innerHTML = "";

        //Clima card
        let clima = chuvas_iuv.lista_previsao[0];
        let previsaoClima = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>Clima</h2>
                        <div class="alertas-temperatura">
                            <p>Máxima: ${clima.maxima} ºC</p>
                            <p>Mínima: ${clima.minima} ºC</p>
                        </div>
                        <p class="alertas-tipo">${clima.tempo_descricao}</p>
                    </div>
                    <img src="/main/resources/assets/images/${clima.categoria}.png" alt="${clima.tempo}-tempo" class="alertas-img" />
                </div>
            `;

        main.innerHTML += previsaoClima;

        //UV card
        let previsaoUV = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>índice UV</h2>
                        <div class="alertas-temperatura">
                            <p>${clima.iuv}</p>
                        </div>
                        <p class="alertas-tipo">${clima.iuv_descricao}</p>
                    </div>
                    <img src="/main/resources/assets/images/ensolarado.png" alt="ensolarado" class="alertas-img" />
                </div>
            `;

        main.innerHTML += previsaoUV;

        //Ondas card
        let onda = ondas.lista_previsao[0];
        let previsaoOndas = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>Ondas</h2>
                        <div class="alertas-temperatura">
                            <p>Altura: ${onda.altura} m</p>
                        </div>
                        <p class="alertas-tipo">${onda.agitacao}</p>
                    </div>
                    <img src="/main/resources/assets/images/ondas.svg" alt="Ondas" class="alertas-img-ondas" />
                </div>
            `;

        main.innerHTML += previsaoOndas;

        //Ventos card
        let previsaoVentos = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>Vento</h2>
                        <p class="alertas-tipo">${onda.vento} km/h</p>
                    </div>
                    <img src="/main/resources/assets/images/vento.svg" alt="Vento" class="alertas-img" />
                </div>
            `;

        main.innerHTML += previsaoVentos;

        console.log(dados);
    }

    /*As categorias do tempo são 6:
        nevada, tempestade, chuvoso, nublado
        parcialmente-nublado e ensolarado*/
});

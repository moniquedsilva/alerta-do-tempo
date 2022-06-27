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

    let titulo = document.getElementById("titulo");
    titulo.innerText = `Bem vindo(a) Monique`;

    let fraseInicio = document.getElementById("texto");
    fraseInicio.innerText = `Previsão do tempo para 27 de junho em Salvador, Bahia.`;

    let main = document.getElementById("alerta");
    main.innerHTML = "";

    //Clima card
    let previsaoClima = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>Clima</h2>
                        <div class="alertas-temperatura">
                            <p>Máxima: 26 ºC</p>
                            <p>Mínima: 24 ºC</p>
                        </div>
                        <p class="alertas-tipo">Chuvoso</p>
                    </div>
                    <img src="/main/resources/assets/images/chuvoso.png" alt="Chuvoso-tempo" class="alertas-img" />
                </div>
            `;

    main.innerHTML += previsaoClima;

    //UV card
    let previsaoUV = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>índice UV</h2>
                        <div class="alertas-temperatura">
                            <p>5.0</p>
                        </div>
                        <p class="alertas-tipo">Moderado</p>
                    </div>
                    <img src="/main/resources/assets/images/ensolarado.png" alt="ensolarado" class="alertas-img" />
                </div>
            `;

    main.innerHTML += previsaoUV;

    let previsaoOndas = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>Ondas</h2>
                        <div class="alertas-temperatura">
                            <p>Altura: 2.17m</p>
                        </div>
                        <p class="alertas-tipo">Alta</p>
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
                        <p class="alertas-tipo">35 km/h</p>
                    </div>
                    <img src="/main/resources/assets/images/vento.svg" alt="Vento" class="alertas-img" />
                </div>
            `;

    main.innerHTML += previsaoVentos;

    /*As categorias do tempo são 6:
        nevada, tempestade, chuvoso, nublado
        parcialmente-nublado e ensolarado*/
});

/*    function respostaDados(dadosJSON) {
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
        let uv = chuvas_iuv.lista_previsao[0].iuv;
        let previsaoUV = `
                <div class="alertas-area">
                    <div class="alertas-texto">
                        <h2>índice UV</h2>
                        <div class="alertas-temperatura">
                            <p>${uv}</p>
                        </div>
                        <p class="alertas-tipo">Alto</p>
                    </div>
                    <img src="/main/resources/assets/images/ensolarado.png" alt="ensolarado" class="alertas-img" />
                </div>
            `;

        main.innerHTML += previsaoUV;

        //Ondas card
        let onda = ondas.manha;
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
*/

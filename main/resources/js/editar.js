window.addEventListener("load", function () {
  //Token csrf
  let tokens = document.getElementsByName("csrfmiddlewaretoken");
  let csrf_token = tokens[0].getAttribute("value");

  //Carrega DropDown de Munícipio assim que carrega a página
  populaMuncipio();
  //Eventos
  //Submit do formulário
  document
      .getElementById("form_edit")
      .addEventListener("submit", submitForm);
  //OnChange do Estado
  document
      .getElementById("estado")
      .addEventListener("change", populaMuncipio);

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

  //Resposta para inserção do cadastro
  function respostaSubmitForm(respostaJSON) {
      let resposta = JSON.parse(respostaJSON);
      if (resposta["status"]) {
        window.location.replace(URL_REDIRECT);
      }
  }

  function populaMuncipio() {
      let xhr = new XMLHttpRequest();
      let url = URL_LOAD_MUNICIPIOS;

      xhr.open("POST", url, true);
      xhr.setRequestHeader("Accept", "application/x-www-form-urlencoded");
      xhr.setRequestHeader(
          "Content-Type",
          "application/x-www-form-urlencoded"
      );
      xhr.setRequestHeader("X-CSRF-Token", csrf_token);

      xhr.onload = () => respostaPopulaMunicipio(xhr.response);
      let formData = new FormData();
      formData.append("csrfmiddlewaretoken", csrf_token);
      formData.append("estado_id", document.getElementById("estado").value);
      let data = new URLSearchParams(formData).toString();
      xhr.send(data);
  }

  function respostaPopulaMunicipio(dadosJSON) {
      let dados = JSON.parse(dadosJSON);
      let select = document.getElementById("municipio");
      select.innerHTML = "";
      for (let d of dados["municipios"]) {
          let opt = document.createElement("option");
          for (let key in d) {
              opt.value = key;
              opt.innerHTML = d[key];
              select.appendChild(opt);
          }
      }
  }
});

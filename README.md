<h1 align="center"> :cloud_with_lightning_and_rain: Alerta do Tempo </h1>

![GitHub repo size](https://img.shields.io/github/repo-size/moniquedsilva/alerta-do-tempo?style=for-the-badge)
![GitHub language count](https://img.shields.io/github/languages/count/moniquedsilva/alerta-do-tempo?style=for-the-badge)
![GitHub contrinutors](https://img.shields.io/github/contributors/moniquedsilva/alerta-do-tempo?style=for-the-badge)
![Bitbucket open issues](https://img.shields.io/bitbucket/issues/moniquedsilva/alerta-do-tempo?style=for-the-badge)
![Bitbucket open pull requests](https://img.shields.io/bitbucket/pr-raw/moniquedsilva/alerta-do-tempo?style=for-the-badge)

<img src="readme/tela.png" alt="exemplo imagem" align="center">

> Cadastre-se na nossa plataforma e confira informações sobre a previsão do tempo relacionadas a chuvas fortes, condições de UV perigosas e/ou ondas marítimas agitadas.

## :earth_americas: Descrição

Sistema Web de previsão do tempo com objetivo de informar sobre a previsão do tempo relacionadas a chuvas fortes, condições de UV perigosas e/ou ondas marítimas agitadas. Iremos utilizar HTML, CSS e Javascript para construir o front-end, Python(Django) para manipular os dados no back-end, MongoDB para o banco de dados, uma API da INPE (Instituto Nacional de Pesquisas Espaciais) para coletarmos dados sobre o tempo em tempo real.

-   ### [Mockup](https://www.figma.com/file/8yBYbRXj2DwAk3MIccJeOc/Alerta-do-Tempo)

## :rocket: Tecnologias

-   <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="">

-   <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="">

-   <img src="https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white" alt="">

-   <img src="https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white" alt="">

-   <img src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" alt="">

## :world_map: Rotas

## :flight_departure: Instalação

Para instalar o <nome_do_projeto>, siga estas etapas:

Linux e macOS:

```
## Clone repositório
git clone https://github.com/moniquedsilva/alerta-do-tempo.git

## Instalar o venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Banco de dados
cp .env.example .env
python manage.py migrate

## Run server
python manage.py runserver

```

## :airplane: Rodando o projeto na sua máquina

## 🤝 Colaboradores

Nossa equipe é composta por:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Konstructa">
        <img src="https://avatars.githubusercontent.com/u/72633880?v=4" width="100px;" alt="Foto da Milena no GitHub"/><br>
        <sub>
          <b>Milena Limoeiro</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/moniquedsilva">
        <img src="https://avatars.githubusercontent.com/u/71049865?v=4" width="100px;" alt="Foto da Monique"/><br>
        <sub>
          <b>Monique Silva</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/yuriKode">
        <img src="https://avatars.githubusercontent.com/u/96872438?v=4" width="100px;" alt="Foto do Yuri"/><br>
        <sub>
          <b> Edson Yuri Silva</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.

[⬆ Voltar ao topo](#alerta-do-tempo)<br>

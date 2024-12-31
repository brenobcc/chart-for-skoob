const mainBtn = document.getElementById("btn_results");
const imgChart = document.getElementById("chart_img");

mainBtn.addEventListener("click", () => {
    console.log("clicado!");
    console.log("carregando img!");
    imgChart.innerHTML = '<img src="static/images/normal-people.jpg" alt="Imagem Exibida" width="300">';
    }
);
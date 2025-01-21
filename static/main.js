document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.form');
    const instructionImage = document.getElementById('instruction-image');
    const loaderGif = '../static/images/loading.gif';

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        instructionImage.src = loaderGif;
        instructionImage.alt = "Carregando...";

        setTimeout(() => {
            form.submit();
        }, 500);
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const burguer = document.getElementById("burguer");
    const nav = document.getElementById("main-nav");

    // Alterna visibilidade do menu ao clicar no ícone hamburguer
    burguer.addEventListener("click", () => {
        if (nav.style.display === "flex") {
            nav.style.display = "none";
        } else {
            nav.style.display = "flex";
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 768) {
            nav.style.display = "flex";
        } else if (!nav.style.display || nav.style.display === "flex") {
            nav.style.display = "none";
        }
    });
});

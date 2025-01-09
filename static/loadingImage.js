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
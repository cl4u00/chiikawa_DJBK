// Abre y cierra el menú de usuario (hamburguesa)
document.addEventListener('DOMContentLoaded', function () {
    var boton = document.querySelector('.hamburger-btn');
    var menu = document.querySelector('.dropdown-menu');
    if (!boton || !menu) { return; }

    boton.addEventListener('click', function (evento) {
        evento.stopPropagation();
        var abierto = menu.classList.toggle('show');
        boton.setAttribute('aria-expanded', abierto);
    });

    document.addEventListener('click', function (evento) {
        if (!menu.contains(evento.target)) {
            menu.classList.remove('show');
            boton.setAttribute('aria-expanded', 'false');
        }
    });
});

function mostrarContenido(idContenido) {
    // Ocultar todos los contenidos
    var todosContenidos = document.getElementsByClassName('contenido_dashboard');
    for (var i = 0; i < todosContenidos.length; i++) {
        todosContenidos[i].style.display = 'none';
    }

    // Mostrar el contenido del botón seleccionado
    var contenido = document.getElementById(idContenido);
    if (contenido) {
        contenido.style.display = 'flex';
    }
}
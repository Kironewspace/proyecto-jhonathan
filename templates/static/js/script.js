// script.js
document.addEventListener("DOMContentLoaded", () => {
    const btnComprar = document.getElementById("btn-comprar");
    const cantidadInput = document.getElementById("cantidad");
    const productoId = parseInt(btnComprar.dataset.productoId, 10);

    btnComprar.addEventListener("click", () => {
        const cantidad = parseInt(cantidadInput.value, 10);

        if (isNaN(cantidad) || cantidad < 1 || cantidad > cantidadInput.max) {
            alert("Por favor, ingresa una cantidad válida.");
            return;
        }

        const url = `http://127.0.0.1:5002/comprar/${productoId}/${cantidad}`;
        window.location.href = url;
    });
});

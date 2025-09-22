function mostrarFormularioProduto() {
    const form = document.getElementById('form-produto');

    // alterna
    if (form.style.display === 'none') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}

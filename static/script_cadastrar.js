function mostrarFormularioProduto() {
    let form = document.getElementById('form-produto');

    // esconde e mostra
    if (form.style.display === 'none') {
        form.style.display = 'block';}

    // } else {
    //     form.style.display = 'none';
    // }
}


async function mostraOpcoesEsalva(event){

    console.log('chamando a função mostra opcoes e salva', event);
    if(event){
        event.preventDefault();
        const form = document.getElementById('formulario_cadastro');
        const formData = new FormData(form); 
        const response = await fetch("/salvar_cadastro", {
            method: "POST",
            mode: 'no-cors',
            body: formData
          });
    }
    let opcoes=document.getElementById('opcoes')

    if (opcoes.style.display === 'none') {
        opcoes.style.display = 'block';}


}
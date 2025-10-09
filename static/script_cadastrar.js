function mostrarFormularioProduto() {
    let form = document.getElementById('form-produto');

    // esconde e mostra
    if (form.style.display === 'none') {
        form.style.display = 'block';}

    // } else {
    //     form.style.display = 'none';
    // }
}

function validarFormulario() {
    const campos = document.querySelectorAll('input[required]');
    let todosPreenchidos = true;

    for (let i = 0; i < campos.length; i++) {
      if (campos[i].value.trim() === '') { // O método trim() remove espaços em branco
        alert(`O campo "${campos[i].id}" é obrigatório.`);
        todosPreenchidos = false;
        break; // Sai do loop assim que encontrar um campo vazio
      }
    }

    return todosPreenchidos;
  }


async function mostraOpcoesEsalva(event){

  if (validarFormulario()){
    console.log('chamando a função mostra opcoes e salva', event);
    if(event){
        event.preventDefault();
        const form = document.getElementById('formulario_cadastro');
        const formData = new FormData(form); 
        const response = await fetch("/cadastrar_usuario", {
            method: "POST",
            mode: 'no-cors',
            body: formData
          });
    }
    let opcoes=document.getElementById('opcoes')

    if (opcoes.style.display === 'none') {
        opcoes.style.display = 'block';}

  }

}


async function salvaProduto(event){

  if (validarFormulario()){
    console.log('chamando a salvar produto', event);
    if(event){
        event.preventDefault();
        const form = document.getElementById('formulario_produto');
        const formData = new FormData(form); 
        const response = await fetch("/salvar_produto", {
            method: "POST",
            mode: 'no-cors',
            body: formData
          });
    }
  }

}
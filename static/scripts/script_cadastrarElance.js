function mostrarFormularioProduto() {
  let form = document.getElementById('form-produto');
  // esconde e mostra
  if (form.style.display === 'none') {
    form.style.display = 'block';
  }
}

function validarFormulario() {
  const campos = document.querySelectorAll('input[required]');
  let todosPreenchidos = true;

  // for (let i = 0; i < campos.length; i++) {
  //   if (campos[i].value.trim() === '') { // O método trim() remove espaços em branco
  //     alert(`O campo "${campos[i].id}" é obrigatório.`);
  //     todosPreenchidos = false;
  //     break; // Sai do loop assim que encontrar um campo vazio
  //   }
  // }

  return todosPreenchidos;
}


async function salva(event) {
  event.preventDefault();

  if (validarFormulario()) {
    console.log('Enviando dados de cadastro...');

    const form = document.getElementById('formulario_cadastro');
    const formData = new FormData(form);

    try {
      const response = await fetch("/cadastrar_usuario", {
        method: "POST",
        body: formData
      });

      if (response.ok) {
        const data = await response.text();
        console.log('Cadastro realizado com sucesso:');
        alert('Usuário cadastrado com sucesso!')
        ;
        window.location.href = "/"; // redireciona se quiser
      } else {
        alert('Erro ao cadastrar o usuário.');
      }

    } catch (error) {
      console.error('Erro no envio:', error);
      alert('Falha na comunicação com o servidor.');
    }
  }
}




// Exemplo: horário vindo do servidor (em UTC)
const horarioUTC = "{{ lance.horario_lance.strftime('%Y-%m-%dT%H:%M:%S') }}Z"; // no seu template Flask
const localTime = new Date(horarioUTC);

// Formata pro horário local do usuário
const horarioLocal = localTime.toLocaleString(undefined, {
  dateStyle: "short",
  timeStyle: "medium"
});

console.log("UTC recebido:", horarioUTC);
console.log("Objeto Date:", localTime);


document.getElementById("horario-lance").textContent = horarioLocal;
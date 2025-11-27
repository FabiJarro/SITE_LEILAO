


function validarFormulario() {
  const campos = document.querySelectorAll('input[required]');
  let todosPreenchidos = true;
  return todosPreenchidos;
}


document.addEventListener("DOMContentLoaded", () => {
  const inputs = document.querySelectorAll(".form-control");

  inputs.forEach((input, index) => {
    input.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();

        const nextIndex = index + 1;

        if (nextIndex < inputs.length) {
          inputs[nextIndex].focus();
        } else {
          document.getElementById("btn-enviar").focus();
          console.log("Último campo. Pressione Enviar ou faça outra ação.");
        }
      }
    });
  });
});



async function enviarFormulario(event) {
  event.preventDefault(); // impede reload da página

  if (validarFormulario()) {
    const form = document.getElementById('formulario_cadastro')
    const formData = new FormData(form)
    const mensagemDiv = document.getElementById("mensagem")

    try {
      const response = await fetch("/cadastrar_usuario", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      mensagemDiv.textContent = "";

      if (data.sucesso) {
        mensagemDiv.textContent = data.mensagem;
        form.reset();
      } else {
        mensagemDiv.textContent = data.mensagem;
      }
    }
    catch (error) {
      console.error("Erro ao enviar formulário:", error);
      alert("Erro inesperado ao cadastrar o usuário.");
    }
  }
}

async function enviarFormularioProduto(event) {
  event.preventDefault(); // impede reload da página

  if (validarFormulario()) {
    const form = document.getElementById('formulario_produto')
    const formData = new FormData(form)
    const mensagemDiv = document.getElementById("mensagem")

    try {
      const response = await fetch("/cadastrar_produto", {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      mensagemDiv.textContent = "";

      if (data.sucesso) {
        mensagemDiv.textContent = data.mensagem;
        form.reset();
      } else {
        mensagemDiv.textContent = data.mensagem;
      }
    }
    catch (error) {
      console.error("Erro ao enviar formulário:", error);
      alert("Erro inesperado ao cadastrar o usuário.");
    }
  }
}




document.addEventListener("DOMContentLoaded", () => {

  const formDeslogado = document.getElementById("form-cadastro-deslogado");
  const btnLance = document.getElementById("btnCadastroDeslogado");

  if (formDeslogado) {
    formDeslogado.addEventListener("submit", (e) => {
      e.preventDefault();
    });
  }

  if (btnLance) {
    btnLance.addEventListener("click", () => {
      document.getElementById("loginMsg").textContent =
        "Você precisa estar logado para cadastrar um produto";

      // Redirecionar sempre para a página inicial
      const urlInicial = "/";
      sessionStorage.setItem("redirecionar_para", urlInicial);

      modal.style.display = "block";
    });
  }

});



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
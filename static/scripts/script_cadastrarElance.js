document.addEventListener("DOMContentLoaded", function () {

  // ----- CPF -----
  const cpf = document.querySelector("#cpf");
  cpf.addEventListener("input", function () {
    let v = cpf.value.replace(/\D/g, "");
    if (v.length > 11) v = v.slice(0, 11);

    if (v.length >= 3) v = v.replace(/(\d{3})(\d)/, "$1.$2");
    if (v.length >= 6) v = v.replace(/(\d{3})(\d)/, "$1.$2");
    if (v.length >= 9) v = v.replace(/(\d{3})(\d{2})$/, "$1-$2");

    cpf.value = v;
  });

  // ----- TELEFONE -----
  const telefone = document.querySelector("#telefone");
  telefone.addEventListener("input", function () {
    let v = telefone.value.replace(/\D/g, "");
    if (v.length > 11) v = v.slice(0, 11);

    if (v.length >= 2) v = v.replace(/(\d{2})(\d)/, "($1) $2");
    if (v.length >= 7) v = v.replace(/(\d{5})(\d)/, "$1-$2");

    telefone.value = v;
  });

  // ----- CEP (xxxxx-xxx) -----
  const cep = document.querySelector("#cep");
  cep.addEventListener("input", function () {
    let v = cep.value.replace(/\D/g, "");
    if (v.length > 8) v = v.slice(0, 8);

    if (v.length >= 6) v = v.replace(/(\d{5})(\d)/, "$1-$2");

    cep.value = v;
  });

  // ----- RG (xx.xxx.xxx-x) -----
  const rg = document.querySelector("#rg");
  rg.addEventListener("input", function () {
    let v = rg.value.replace(/\D/g, "");
    if (v.length > 9) v = v.slice(0, 9);

    if (v.length >= 2) v = v.replace(/(\d{2})(\d)/, "$1.$2");
    if (v.length >= 5) v = v.replace(/(\d{3})(\d)/, "$1.$2");
    if (v.length >= 8) v = v.replace(/(\d{3})(\d)$/, "$1-$2");

    rg.value = v;
  });

  // ----- VERIFICAR SENHAS IGUAIS -----
  const senha = document.querySelector("#senha");
  const confirmar = document.querySelector("#confirmarsenha");
  const mensagem = document.querySelector("#mensagem");
  const botao = document.querySelector("#btn-enviar");

  function verificarSenhas() {
    if (senha.value === "" || confirmar.value === "") {
      mensagem.innerHTML = "";
      botao.disabled = false;
      return;
    }

    if (senha.value !== confirmar.value) {
      mensagem.style.color = "red";
      mensagem.textContent = "As senhas não coincidem!";
      botao.disabled = true;
    } else {
      mensagem.style.color = "green";
      mensagem.textContent = "✔ Senhas coincidem!";
      botao.disabled = false;
    }
  }

  senha.addEventListener("input", verificarSenhas);
  confirmar.addEventListener("input", verificarSenhas);


});

document.addEventListener("DOMContentLoaded", () => {

  const dataInput = document.querySelector("#data_nascimento");

  // MÁSCARA BRASILEIRA DD/MM/AAAA
  dataInput.addEventListener("input", (e) => {
      let v = e.target.value.replace(/\D/g, "");

      if (v.length > 2 && v.length <= 4) {
          v = v.replace(/(\d{2})(\d{1,2})/, "$1/$2");
      } 
      else if (v.length > 4) {
          v = v.replace(/(\d{2})(\d{2})(\d{1,4})/, "$1/$2/$3");
      }

      e.target.value = v;
  });

  // CONVERTER PARA AAAA-MM-DD ANTES DE ENVIAR
  document.querySelector("#btn-enviar").addEventListener("click", () => {
      let valor = dataInput.value;

      if (!/^\d{2}\/\d{2}\/\d{4}$/.test(valor)) {
          alert("Data inválida. Use o formato DD/MM/AAAA.");
          return;
      }

      let partes = valor.split("/");
      let dia = partes[0];
      let mes = partes[1];
      let ano = partes[2];

      // Converte para ISO (AAAA-MM-DD)
      let formatoISO = `${ano}-${mes}-${dia}`;

      // substitui no input antes de enviar
      dataInput.value = formatoISO;

      document.querySelector("#formulario_cadastro").submit();
  });

});



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


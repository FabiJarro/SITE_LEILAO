// function carregar_mini_secao() {
//     fetch('minhaconta.html') // Faz a requisição ao arquivo
//       .then(response => response.text()) // Converte a resposta em texto
//       .then(html => {
//         document.getElementById('conteudo-dinamico').innerHTML = html; // Insere o HTML na div
//       })
//       .catch(error => {
//         console.error('Erro ao carregar o conteúdo:', error);
//       });
//   }



//   function carregar_mini_secao(secao) {
//     let conteudoDiv = document.getElementById("conteudo-dinamico");

//     if (secao === "meus_dados") {
//         conteudoDiv.innerHTML = "<h2>Meus dados</h2><p>Aqui vão as informações do usuário.</p>";
//     } 
//     else if (secao === "meus_lances") {
//         conteudoDiv.innerHTML = "<h2>Meus lances</h2><p>Aqui aparece o histórico de lances.</p>";
//     } 
//     else if (secao === "produtos_leiloados") {
//         conteudoDiv.innerHTML = "<h2>Produtos leiloados</h2><p>Lista dos produtos que você leiloou.</p>";
//     }
// }

async function carregarConteudo(secao) {
    const conteudoDiv = document.getElementById("conteudo-dinamico");

    try {
        const response = await fetch(`/minhaconta/${secao}`);
        if (!response.ok) {
            throw new Error("Erro ao carregar conteúdo");
        }

        const html = await response.text();
        conteudoDiv.innerHTML = html;

    } catch (error) {
        conteudoDiv.innerHTML = `${error.message}`;
    }
}
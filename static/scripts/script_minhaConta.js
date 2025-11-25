

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
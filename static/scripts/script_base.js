//modal
var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];

if (btn) {
    btn.onclick = function () {
        modal.style.display = "block";
    };
}


span.onclick = function () {
    modal.style.display = "none";
};

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};



//login
document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    const resposta = await fetch("/entrar_usuario", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ email, senha }),
    });

    if (resposta.redirected) {
        // Login OK: fecha modal e recarrega página
        modal.style.display = "none";
        window.location.href = resposta.url;
    } else {
        const msg = document.getElementById("loginMsg");
        msg.textContent = "Usuário ou senha incorretos!";
    }
});



document.addEventListener("DOMContentLoaded", () => {
    const btnMenu = document.getElementById("btnMenu");
    const menuDropdown = document.getElementById("menuDropdown");

    btnMenu.addEventListener("click", () => {
        menuDropdown.style.display =
            menuDropdown.style.display === "flex" ? "none" : "flex";
    });
});


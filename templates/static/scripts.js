// ------- POP-UP -------
document.addEventListener("DOMContentLoaded", function () {

    const popup = document.getElementById("popup");
    const popupClose = document.getElementById("popupClose");

    // -----------------------------
    // Abrir popup ao clicar na chave
    // -----------------------------
    document.querySelectorAll(".chave-item").forEach(item => {
        item.addEventListener("click", function () {

            // Título
            let titulo = this.querySelector(".chave-numero").innerText;
            document.getElementById("popupTitulo").innerText = titulo;

            // Hora da ação
            const agora = new Date();
            const hora = agora.toLocaleString("pt-BR", {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit"
            });

            document.getElementById("popupHora").innerText = "Hora da ação: " + hora;

            // Status
            let status = this.querySelector(".chave-status").innerText;
            document.getElementById("popupStatus").innerText = status;

            popup.style.display = "flex";
        });
    });

    // -----------------------------
    // Botão FECHAR (X)
    // -----------------------------
    popupClose.addEventListener("click", () => {
        popup.style.display = "none";
    });

    // Botão CANCELAR
    const btnCancelar = document.querySelector(".btn-cancelar");
    if (btnCancelar) {
        btnCancelar.addEventListener("click", () => {
            popup.style.display = "none";
        });
    }

    // -----------------------------
    // Fechar clicando fora
    // -----------------------------
    window.addEventListener("click", function (e) {
        if (e.target === popup) {
            popup.style.display = "none";
        }
    });

    // -----------------------------
    // Fechar com ESC
    // -----------------------------
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            popup.style.display = "none";
        }
    });

});
// ------- FIM POP-UP -------

//-----------------TEMPORIZADOR----------------------\\
let tempoSemAtividade = 0;
    let tempoParaAviso = 1000; // 10s sem atividade para começar alerta
    let tempoParaLogout = 10; // 10s após o alerta para deslogar

    let aviso = document.getElementById("logout-warning");
    let numero = document.getElementById("contador");

    aviso.style.display = "none";

    // Reseta o tempo ao detectar atividade
    function resetarInatividade() {
        tempoSemAtividade = 0;
        aviso.style.display = "none";
    }

    // Eventos de atividade
    document.onmousemove = resetarInatividade;
    document.onkeypress = resetarInatividade;
    document.onclick = resetarInatividade;
    document.onscroll = resetarInatividade;

    setInterval(() => {
        tempoSemAtividade++;

        // Se o usuário ficar 10s sem mexer → começa contagem do aviso
        if (tempoSemAtividade >= tempoParaAviso && tempoSemAtividade < tempoParaAviso + tempoParaLogout) {
            aviso.style.display = "block";
            let restante = (tempoParaAviso + tempoParaLogout) - tempoSemAtividade;
            numero.textContent = restante;
        }

        // Se chegar ao final da contagem → desloga automaticamente
        if (tempoSemAtividade >= tempoParaAviso + tempoParaLogout) {
            document.getElementById("logoutForm").submit();
        }

    }, 1000);


// ------- POP-UP -------
document.addEventListener("DOMContentLoaded", function () {

    const popup = document.getElementById("popup");
    const popupClose = document.getElementById("popupClose");

    let dadosChaveSelecionada = null; // <- Vamos usar para enviar ao backend depois

    // -----------------------------
    // Abrir popup ao clicar na chave
    // -----------------------------
    document.querySelectorAll(".chave-item").forEach(item => {
        item.addEventListener("click", function () {

            // ----- Dados vindos dos atributos data-* -----
            const chaveId = this.dataset.chave;
            const pessoaNome = this.dataset.pessoa;   // string vazia se disponível
            const checkin = this.dataset.checkin;
            const statusDB = this.dataset.status;     // True / False (string)

            // Guardar para o backend
            dadosChaveSelecionada = {
                chaveId: chaveId,
                pessoaNome: pessoaNome,
                checkin: checkin,
                statusDB: statusDB
            };

            // ----- Status visível ("Disponível" ou "Posse: Fulano") -----
            const statusTexto = this.querySelector(".chave-status").innerText.trim();
            const statusNomeChave = this.querySelector(".chave-local").innerText.trim();
            // Decidir ação (retirar/devolver)
            let acaoPopup;
            if (statusTexto === "Disponível") {
                acaoPopup = "Retirar";
                dadosChaveSelecionada.acao = "retirar";
            } else {
                acaoPopup = "Devolver";
                dadosChaveSelecionada.acao = "devolver";
            }

            // ----- Título -----
            const titulo = this.querySelector(".chave-numero").innerText;
            document.getElementById("popupTitulo").innerText = `Ação: ${acaoPopup} ${titulo} - ${statusNomeChave}`;

            // ----- Hora da ação -----
            const agora = new Date();
            const hora = agora.toLocaleString("pt-BR", {
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit"
            });
            document.getElementById("popupHora").innerText = "Hora da ação: " + hora;

            // ----- Usuário -----
            let user = document.getElementById("usuario-logado").dataset.nome;
            document.getElementById("popupUsuario").innerText = "Usuário: " + user;

            // Abrir popup
            popup.style.display = "flex";
        });
    });



    // -----------------------------
    // Botão CONFIRMAR
    // -----------------------------
    const btnConfirmar = document.getElementById('popup-chaves-btn-confirmar')

    btnConfirmar.addEventListener("click", () => {
        
    })
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

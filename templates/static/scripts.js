//-----------------TEMPORIZADOR----------------------\\
let tempoSemAtividade = 0;
    let tempoParaAviso = 1000; // 10s sem atividade para começar alerta
    let tempoParaLogout = 5; // 10s após o alerta para deslogar

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
    const btnConfirmar = document.getElementById('popup-chaves-btn-confirmar')
    const popup = document.getElementById("popup");
    const popupClose = document.getElementById("popupClose");

    let dadosChaveSelecionada = null; // <- Vamos usar para enviar ao backend depois

     //------ Dados vindos de status_chaves.html-------------\\  
                    //TODOS OS DADOS DE USER\\
    const usuarioLogado = document.getElementById("usuario-logado").dataset;
    const nomeUsuario = usuarioLogado.nome;
    const pessoaMatricula = usuarioLogado.matricula;

    
                // -----------------------------
                // Abrir popup ao clicar na chave
                // -----------------------------
    document.querySelectorAll(".chave-item").forEach(item => {
        item.addEventListener("click", function () {
            // COLOCANDO AQUI TODAS AS VARIÁVEIS
       
        // ----- Dados vindos dos atributos data-* em chave_item.html-----
                    //TODOS OS DADOS DE CHAVE
            const dadosChave = this.dataset;
            const chaveId = dadosChave.chave;
            const statusChave = (dadosChave.status === "True");
            const chaveNome = dadosChave.chaveNome;
            const acao = statusChave ? "RETIRADA" : "DEVOLUCAO";
            const acaoPopup = acao === "RETIRADA" ? "Retirar" : "Devolver";
            
            document.getElementById("popupTitulo").innerText = `Ação: ${acaoPopup} Chave ${chaveId} - ${chaveNome}`;

            // ----- Hora da ação -----
            const agora = new Date();
            const dataHora = agora.toLocaleString("pt-BR", {
                day: "2-digit",
                month: "2-digit",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit"
            });

            dadosChaveSelecionada = {
                chave: chaveId,
                pessoa: pessoaMatricula,
                acao: acao
            }

            document.getElementById("popupHora").innerText = "Data e hora da ação: " + dataHora;

            // ----- Usuário -----
            document.getElementById("popupUsuario").innerText =
            "Usuário: " + nomeUsuario;
            // Abrir popup
            popup.style.display = "flex";
        });
    });



    // -----------------------------
    // Botão CONFIRMAR
    // -----------------------------
    

    btnConfirmar.addEventListener("click", () => {

    if (!dadosChaveSelecionada) return;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch("/atualizar-status/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": csrftoken
        },
        body: new URLSearchParams({
            chave_id: dadosChaveSelecionada.chave,
            pessoa_id: dadosChaveSelecionada.pessoa,
            acao: dadosChaveSelecionada.acao
        })
    })

    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            location.reload();
            popup.style.display = "none";
        } else {
            alert("Erro: " + data.erro);
        }
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


//----------------inicio filtros---------------------
document.addEventListener("DOMContentLoaded", function () {

    function carregarResultados(params) {
    const queryString = new URLSearchParams(params).toString();

    fetch(`?${queryString}`, {
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector(".status-container").innerHTML = data.html;
        aplicarEventosPaginacao();  // Reaplicar eventos após atualizar HTML
    });
}


    // ===== FILTRO =====
    const filtroForm = document.querySelector("#filtro-form");

    filtroForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const params = {
            busca: this.busca.value,
            status: this.status.value || "",
            page: 1
        };

        carregarResultados(params);
    });



    // ===== PAGINAÇÃO AJAX =====
    function aplicarEventosPaginacao() {
    document.querySelectorAll(".ajax-page").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const page = this.dataset.page;

            const busca = document.querySelector("input[name=busca]").value;
            const status = document.querySelector("input[name=status]:checked")?.value || "";

            carregarResultados({ busca, status, page });
        });
    });
}


    aplicarEventosPaginacao();
});

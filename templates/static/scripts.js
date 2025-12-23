//-----------------TEMPORIZADOR----------------------\\
let tempoSemAtividade = 0;
    let tempoParaAviso = 10; // 10s sem atividade para começar alerta
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

/* ================================
   FUNÇÃO PRINCIPAL DO POPUP
================================ */
function aplicarEventosPopup() {
    const popup = document.getElementById("popup");
    const popupClose = document.getElementById("popupClose");
    const btnConfirmar = document.getElementById("popup-chaves-btn-confirmar");
    const btnCancelar = document.querySelector(".btn-cancelar");

    let dadosChaveSelecionada = null;

    /* ========== DADOS DO USUÁRIO LOGADO ========== */
    const usuario = document.getElementById("usuario-logado").dataset;
    const nomeUsuario = usuario.nome;
    const pessoaMatricula = usuario.matricula;

    /* ========== FUNÇÃO: ABRIR POPUP ========== */
    function abrirPopup(dadosChave) {
        const chaveId = dadosChave.chave;
        const chaveNome = dadosChave.chaveNome;
        const statusChave = (dadosChave.status === "True");

        const acao = statusChave ? "RETIRADA" : "DEVOLUCAO";
        const acaoPopup = statusChave ? "Retirar" : "Devolver";

        document.getElementById("popupTitulo").innerHTML =
            `<strong>Ação:</strong> ${acaoPopup} Chave ${chaveId} - ${chaveNome}`;


        dadosChaveSelecionada = {
            chave: chaveId,
            pessoa: pessoaMatricula,
            acao: acao
        };

        const agora = new Date().toLocaleString("pt-BR");
        document.getElementById("popupHora").innerHTML = `<strong>Data e hora da ação:</strong> ${agora}`;

        document.getElementById("popupUsuario").innerHTML = `<strong>Usuário:</strong> ${nomeUsuario}`;


        popup.style.display = "flex";
    }

    /* ========== FUNÇÃO: ADICIONAR EVENTOS NOS ITENS ========== */
    function aplicarEventosItens() {
        document.querySelectorAll(".chave-item").forEach(item => {
            item.addEventListener("click", () => {
                abrirPopup(item.dataset);
            });
        });
    }

    /* ========== FUNÇÃO: CONFIRMAR AÇÃO ========== */
    function confirmarAcao() {
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
        .then(r => r.json())
        .then(data => {
            if (data.sucesso) {
                location.reload();
            } else {
                alert("Erro: " + data.erro);
            }
        });
    }

    /* ========== EVENTOS FIXOS ========== */
    if (btnConfirmar) btnConfirmar.addEventListener("click", confirmarAcao);
    if (btnCancelar) btnCancelar.addEventListener("click", () => popup.style.display = "none");
    if (popupClose) popupClose.addEventListener("click", () => popup.style.display = "none");

    /* ========== APLICA OS EVENTOS INICIAIS ========== */
    aplicarEventosItens();

    /* 
       IMPORTANTE:
       Quando você carregar a lista via AJAX, precisa chamar novamente
       aplicarEventosItens() — por isso a função é separada.
    */
}

/* ========== EXECUTA AO CARREGAR A PÁGINA ========== */
document.addEventListener("DOMContentLoaded", aplicarEventosPopup);


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
        aplicarEventosPopup();
    });
}


    // ===== FILTRO =====
    const filtroForm = document.querySelector("#filtro-form");
    const inputBusca = filtroForm.querySelector("input[name=busca]");
    const radiosStatus = filtroForm.querySelectorAll("input[name=status]");

    // Aplicar ao digitar (com pequeno delay)
    let typingTimer;
    inputBusca.addEventListener("input", function () {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(() => {
            const params = {
                busca: inputBusca.value,
                status: filtroForm.status.value,
                page: 1
            };
            carregarResultados(params);
        }, 300); // delay anti-spam
    });

    // Aplicar ao clicar nos radios
    radiosStatus.forEach(r => {
        r.addEventListener("change", function () {
            const params = {
                busca: inputBusca.value,
                status: this.value,
                page: 1
            };
            carregarResultados(params);
        });
    });



    // ===== PAGINAÇÃO AJAX =====
    function aplicarEventosPaginacao() {
    document.querySelectorAll(".ajax-page").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const page = this.dataset.page;

            const busca = document.querySelector("input[name=busca]").value;
            const status = document.querySelector("input[name=status]:checked")?.value || "none";

            carregarResultados({ busca, status, page });
        });
    });
}
// ===== BUSCA PARCIAL =====

// Função debounce para evitar várias requisições por segundo
function debounce(func, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}

inputBusca.addEventListener("input", debounce(function () {
    const busca = this.value;
    const status = document.querySelector("input[name=status]:checked")?.value || "";

    carregarResultados({ busca, status, page: 1 });
}, 300)); // 300ms é o ideal


    aplicarEventosPaginacao();
});


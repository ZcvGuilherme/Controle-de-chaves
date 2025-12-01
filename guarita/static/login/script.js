let tempoSemAtividade = 0;
    let tempoParaAviso = 60; // 10s sem atividade para começar alerta
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

    console.log("JS carregou ✔"); // TESTE — deve aparecer no console

    document.querySelectorAll(".chave-item").forEach(item => {
        item.addEventListener("click", function(){
            let titulo = this.querySelector(".chave-numero").innerText;
            let local = this.querySelector(".chave-local").innerText;
            let status = this.querySelector(".chave-status").innerText;

            document.getElementById("popupTitulo").innerText = titulo;
            document.getElementById("popupLocal").innerText  = "Local: " + local;
            document.getElementById("popupStatus").innerText = status;

            document.getElementById("popup").style.display = "flex";
        });
    });

    document.getElementById("popupClose").onclick = () =>
        document.getElementById("popup").style.display = "none";

});
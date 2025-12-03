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
// ------- FIM POP-UP -------

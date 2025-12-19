// SCRIPT GENERER PAR IA
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("fichiers");
    const bouton = document.querySelector(".btn-select-files");
    const compteur = document.querySelector(".compteur-fichiers");
    const liste = document.querySelector(".liste-fichiers");

    let fichiersAjoutes = [];

    bouton.addEventListener("click", () => input.click());

    input.addEventListener("change", () => {
        const nouveauxFichiers = Array.from(input.files);
        fichiersAjoutes = fichiersAjoutes.concat(nouveauxFichiers);

        // Mise à jour du compteur
        const nb = fichiersAjoutes.length;
        compteur.textContent = nb === 0 ? "Aucun fichier sélectionné ❌" :
            nb === 1 ? "1 fichier sélectionné 📁" : `${nb} fichiers sélectionnés 📂`;

        // Liste des fichiers
        liste.innerHTML = "";
        fichiersAjoutes.forEach(fichier => {
            const li = document.createElement("li");
            li.innerHTML = `<i class="icon-upload">📄</i> <span>${fichier.name}</span>`;
            liste.appendChild(li);
        });
    });
});

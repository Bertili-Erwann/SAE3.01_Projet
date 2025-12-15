function afficheFichier() {
  const divFichier = document.getElementById("fichier");
  if (
    document.getElementById("eleve-0").checked &&
    document.getElementById("eleve-0").value == "Oui"
  ) {
    divFichier.classList.remove("hidden");
  } else {
    divFichier.classList.add("hidden");
  }
} 
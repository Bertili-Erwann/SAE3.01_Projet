function afficheFichier() {
  const divFichier = document.getElementById("fichier");
  if (
    document.getElementById("eleve-0").checked &&
    document.getElementById("eleve-0").value == "Oui"
  ) {
    divFichier.innerHTML = `
                <label for="justificatif">Justificatif</label>
                <input type="file" id="justificatif" accept="image/png, image/jpeg, .pdf" />`;
  } else {
    divFichier.replaceChildren();
  }
}

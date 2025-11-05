function spawnJustificatif() {
  const divFichier = document.getElementById("fichier");
  if (!divFichier) return;
  if (document.getElementById("oui").checked) {
    divFichier.innerHTML = `
                <label for="justificatif">Justificatif</label>
                <input type="file" id="justificatif" accept="image/png, image/jpeg, .pdf" />`;
  } else {
    divFichier.innerHTML = "";
  }
}
function killJustificatif() {
  const divFichier = document.getElementById("fichier");
  if (!divFichier) return;
  if (document.getElementById("non").checked) {
    divFichier.replaceChildren();
  }
}

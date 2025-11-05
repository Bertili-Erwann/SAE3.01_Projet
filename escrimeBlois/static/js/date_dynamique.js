document.addEventListener("DOMContentLoaded", function () {
  const dateInput = document.getElementById("date-naissance");
  const formDyna = document.getElementById("form-dyna");
  if (!dateInput || !formDyna) return;

  dateInput.addEventListener("input", function () {
    const dateAuj = new Date();
    const inputValue = dateInput.value;
    const naiss = new Date(inputValue);
    if (isNaN(naiss)) {
      formDyna.innerHTML = "";
      return;
    }

    let age = dateAuj.getFullYear() - naiss.getFullYear();
    const monthDiff = dateAuj.getMonth() - naiss.getMonth();
    if (
      monthDiff < 0 ||
      (monthDiff === 0 && dateAuj.getDate() < naiss.getDate())
    ) {
      age--;
    }

    if (age >= 18) {
      formDyna.innerHTML = `
    <label for="etudiant">
      8. Êtes-vous étudiant(e) ? <span id="obligatoire">*</span>
    </label>
      <div>
        <input type="radio" name="justificatif" value="Oui" id="oui" onclick="spawnJustificatif()" />
        <label for="est_etudiant"> Oui </label>
        <input type="radio" name="justificatif" value="Non" id="non" onclick="killJustificatif()"/>
        <label for="est_etudiant">Non</label>
        <div id="fichier"> </div>
      </div>
    `;
    } else {
      formDyna.innerHTML = `
    <label for="scolarise">
      8. Êtes-vous scolarisé(e) ? <span id="obligatoire">*</span>
    </label>
      <div class ="block-scolarise">
        <input type="radio" name="justificatif" value="Oui" id="oui" onclick="spawnJustificatif()" />
        <label for="est_scolarise"> Oui </label>
        <input type="radio" name="justificatif" value="Non" id="non" onclick="killJustificatif()" />
        <label for="est_scolarise">Non</label>
        <div id="fichier"> </div>
      </div>
    `;
    }
  });
});

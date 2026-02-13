// Généré par gemini

function togglePassword(inputId, icon) {
    const input = document.getElementById(inputId);
    if (input.type === "password") {
        input.type = "text";
        icon.textContent = "🔒"; // Icône quand le mdp est visible (pour le recacher)
    } else {
        input.type = "password";
        icon.textContent = "👁️"; // Icône quand le mdp est caché
    }
}

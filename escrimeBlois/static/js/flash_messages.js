// Auto-fermer les messages flash après 5 secondes
document.addEventListener('DOMContentLoaded', function() {
    const flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        setTimeout(function() {
            const alert = new bootstrap.Alert(flashMessage);
            alert.close();
        }, 5000);
    }
});

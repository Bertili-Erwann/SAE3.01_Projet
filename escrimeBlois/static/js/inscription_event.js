document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('inscription_success')) {
        var successModalElement = document.getElementById('successInscriptionModal');
        if (successModalElement) {
            var myModal = new bootstrap.Modal(successModalElement);
            myModal.show();
        }
    }
});
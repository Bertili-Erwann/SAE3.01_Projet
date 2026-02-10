tinymce.init({
    selector: '#contenu-editor',
    height: 400,
    plugins: 'advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table help wordcount',
    toolbar: 'undo redo | formatselect | bold italic backcolor | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | removeformat | help | code',
    valid_elements: '*[*]', // Autorise tous les éléments et attributs
    extended_valid_elements: '*[*]',
    verify_html: false, // Désactive le nettoyage HTML
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:14px }'
});

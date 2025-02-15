function copyUrl() {
    // Get the text field
    var copyText = document.getElementById("shortUrlInput");
    console.log(copyText)
    // Select the text field
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices
  
     // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value);
  }


  document.getElementById('registrationForm').addEventListener('submit', function (event) {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const errorElement = document.getElementById('passwordError');

    if (password !== confirmPassword) {
        errorElement.textContent = 'Password confirmation does not match';
        event.preventDefault(); // Evita que el formulario se envíe
    } else {
        errorElement.textContent = ''; // Limpia el mensaje de error
    }
});
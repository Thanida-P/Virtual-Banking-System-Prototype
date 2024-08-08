function displaySelectedImage(event, elementId) {
    const selectedImage = document.getElementById(elementId);
    const fileInput = event.target;

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            selectedImage.src = e.target.result;
        };

        reader.readAsDataURL(fileInput.files[0]);
    }
}

function showPassword(num) {
    if (num == 1) {
        var pass = document.getElementById("password");
    } else {
        var pass = document.getElementById("confirmPassword");
    }
    
    if (pass.type === "password") {
        pass.type = "text";
    } else {
        pass.type = "password";
    }
}

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

const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
});

async function signUp() {
    const middleName = document.getElementById('middlename').value;
    const form = document.getElementById('signUpForm');
    const formData = new FormData(form);
    
    const requiredFields = form.querySelectorAll('input:not(#middlename), select');
    let isValid = true;
    let isCheckbox = false;

    requiredFields.forEach(field => {
        if ((field.type !== 'file' && field.type !== 'checkbox' && field.value.trim() === '') || 
            (field.type === 'checkbox' && !field.checked)) {
            if (field.type === 'checkbox' && !field.checked) {
                isCheckbox = true;
            }
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    if (!isValid) {
        alert('Please fill in all required fields.');
        if (isCheckbox) {
            alert('Please agree to the term of services.');
        }
        return;
    }

    const fileInput = form.querySelector('input[type="file"]');
    const file = fileInput.files[0];

    if (file) {

        const formObject = {};
        formData.forEach((value, key) => {
            formObject[key] = value;
        });

        formObject.file = await toBase64(file);
        formObject.filename = file.name;

        fetch('/signUpSubmission', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formObject),

        }).then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    alert(data.detail)
                });
            } else {
                return response.json() .then(data => {
                    alert('Account created successfully!');
                    window.location.href = '/login';
                })
            }
        }).catch(error => console.error('Error:', error));

    } else {
        alert('Please upload a profile picture');
    }
}

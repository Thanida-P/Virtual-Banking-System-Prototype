async function addAdmin() {
    const form = document.getElementById('add-admin-form');
    const formData = new FormData(form);

    const formObject = {};
    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    const response = await fetch('/addAdmin', {
        method: 'POST',
        body: JSON.stringify(formObject),
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        alert('Admin added successfully!');
        form.reset();
        window.location.href = '/login';
    } else {
        alert('Please enter all required fields');
    }
}
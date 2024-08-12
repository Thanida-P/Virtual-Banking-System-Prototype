async function addAccount() {
    const form = document.getElementById('add-account-form');
    const formData = new FormData(form);

    const formObject = {};

    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    const response = await fetch('/addAccount', {
        method: 'POST',
        body: JSON.stringify(formObject),
        headers: {
            'Content-Type': 'application/json'
        }
    });
    console.log(response);
    if (response.ok) {
        alert('Account added successfully!');
        form.reset();
        window.location.href = '/home';
    } else {
        const errorText = await response.text(); // Read the response text
        alert(`Problem adding account: ${response.status} - ${errorText}`);
    }
}
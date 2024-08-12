function displayAccount(accountDict) {
    let carouselIndicators = document.getElementById('carousel-indicators');
    let carouselInner = document.getElementById('carousel-inner');
    let isFirst = true;

    carouselIndicators.innerHTML = '';
    carouselInner.innerHTML = ''; 

    for (let key in accountDict) {
        let account = accountDict[key];

        let indicator = document.createElement('li');
        indicator.setAttribute('data-bs-target', '#owned_accounts');
        indicator.setAttribute('data-bs-slide-to', Object.keys(accountDict).indexOf(key));
        if (isFirst) {
            indicator.classList.add('active');
            isFirst = false;
        }
        carouselIndicators.appendChild(indicator);

        // Create carousel item
        let item = document.createElement('div');
        item.classList.add('carousel-item');
        if (Object.keys(accountDict).indexOf(key) === 0) {
            item.classList.add('active');
        }

        // Create account info
        let accountType;
        switch (account.bankType) {
            case 'savings':
                accountType = 'Savings Account';
                break;
            case 'checking':
                accountType = 'Checking Account';
                break;
            case 'business':
                accountType = 'Business Account';
                break;
            default:
                accountType = 'Other Account';
                break;
        }

        item.innerHTML = `
            <div class="account-info">
                <h5>${accountType}</h5>
                <p>Balance: &#3647;${account.balance}</p>
                <p class="account-num">Account Number: ${account.accountNumber}</p>
            </div>
        `;

        carouselInner.appendChild(item);
    }
}

function generate_otp() {
    return Math.random().toString(36).slice(2, 8);
}

function getAccountFromCard() {
    const activeCarouselItem = document.querySelector('.carousel-item.active');
    const accountNumber = activeCarouselItem.querySelector('.account-num').textContent.split(' ')[2];

    return accountNumber;
}


function proceed() {
    const phoneNo = document.getElementById('phno').value;
    const amount = document.getElementById('amount').value;
    const action = document.getElementById('action').value;
    const accountNumber = getAccountFromCard();

    if (phoneNo && amount && action && accountNumber) {
        // Assume the validation is successful and you have an OTP generated
        const otp = generate_otp();

        // Set the OTP in the modal
        document.getElementById('otp').innerText = otp;
        document.getElementById('otp').value = otp;

        // Show the modal
        $('#transactionOtpModal').modal('show');
    } else {
        alert("Please fill out all required fields.");
    }
}

async function confirmOtp() {
    const otp = document.getElementById('otp').value;
    const form = document.getElementById('transaction-form');
    const formData = new FormData(form);

    const formObject = {};

    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    formObject['banknumber'] = getAccountFromCard();
    formObject['otp'] = otp;

    console.log(JSON.stringify(formObject));

    const response = await fetch('/transaction', {
        method: 'POST',
        body: JSON.stringify(formObject),
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        alert('Transaction successful!');
        $('#transactionOtpModal').modal('hide');
        location.reload();
    } else {
        alert('An error occurred. Please try again later.');
    }
}

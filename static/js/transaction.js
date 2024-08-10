var carousel = new bootstrap.Carousel('#accounts', {
    interval: false,
    ride: false
});

function displayAccount(accountDict) {
    let accounts = document.getElementById('accounts');
    let carouselIndicators = document.getElementById('carousel-indicators');
    let carouselInner = document.getElementById('carousel-inner');
    let remainingLimitElement = document.getElementById('remaining-limit');

    let isFirst = true;

    // Clear existing indicators and items
    carouselIndicators.innerHTML = '';
    carouselInner.innerHTML = '';

    // Iterate over accountDict and create carousel items and indicators
    for (let key in accountDict) {
        let account = accountDict[key];

        // Create carousel indicator
        let indicator = document.createElement('li');
        indicator.setAttribute('data-bs-target', '#accounts');
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

        formmattedBalance = account.balance.toFixed(2);

        item.innerHTML = `
            <div class="account-info">
                <h5>${accountType}</h5>
                <p>Balance: &#3647;${formmattedBalance}</p>
                <p>Account Number: ${account.accountNumber}</p>
            </div>
        `;

        carouselInner.appendChild(item);
    }

    // Refresh carousel
    carousel.refresh();
}

function selectedAccount() {
    let accounts = document.getElementById('accounts');
    let accountID = accounts.querySelector('.active').querySelector('.account-info').querySelector('p').innerText.split(' ')[2];
    let balance = accounts.querySelector('.active').querySelector('.account-info').querySelector('p').innerText.split(' ')[1].split(';')[1];

    
    fetch(`/transaction`, {
        method: 'POST',
        body: `{"selectedAccount": "${accountID}"}`,
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
    })
}

function generate_otp() {
    otp = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6));
    document.getElementById("otp").value = otp;
    return otp
}

function proceedWithraw() {
    // Check if all fields are filled
    let action = document.getElementById("action").value;
    let phoneNo = document.getElementById("phone-no").value;
    let amount = document.getElementById("amount").value;
    let otp = document.getElementById("otp").value;

    if (action && phoneNo && amount) {
        // Show the OTP modal
        $('#transactionOtpModal').modal('show');

        // Generate and display the OTP
        let otp = generate_otp();
        document.getElementById("rotp").innerHTML = otp;

        // Set the OTP in the form
        document.getElementById("otp").value = otp;

    } else {
        alert("Please fill out all fields.");
    }
}

// Handle the OK button click inside the modal
document.getElementById("confirmOtpButton").addEventListener("click", function() {
    // Submit the form or perform the transaction
    document.getElementById("transaction-form").submit();
});

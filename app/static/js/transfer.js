function reviewTransfer() {
    const form = document.getElementById("transfer-form");
    const formData = new FormData(form);

    let formObject = {};
    
    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    if (Object.keys(formObject).length === 2) {
        alert("Please fill in all required fields");
        return;
    }

    for (let key in formObject) {
        if (formObject[key] === "") {
            alert("Please fill in all required fields");
            return;
        }
    }
    
    formObject["banknumber"] = getAccountFromCard();
    
    fetch('/transferReview', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formObject)
    }).then(response => {
        if (response.ok) {
            response.json().then(data => {
                url_parameter = btoa('transferId=' + data.transferId);
                window.location.href = '/transferReview/' + url_parameter;
            });
        }
    })
}

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

function getAccountFromCard() {
    const activeCarouselItem = document.querySelector('.carousel-item.active');
    const accountNumber = activeCarouselItem.querySelector('.account-num').textContent.split(' ')[2];

    return accountNumber;
}


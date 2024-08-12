
function displayPicture(filename) {
    profile = document.getElementById('profile-image');

    avatarDisplay =
    '<img src="' +
    window.location.origin +
    "/static/profile/" +
    filename +
    '" alt="avatar" class="rounded-circle img-fluid" style="width: 125px;" />';

    profile.innerHTML = avatarDisplay;
  
}


function displayAccount(accountDict) {
    let accounts = document.getElementById('accounts');
    let carouselIndicators = document.getElementById('carousel-indicators');
    let carouselInner = document.getElementById('carousel-inner');

    let isFirst = true;

    carouselIndicators.innerHTML = '';
    carouselInner.innerHTML = '';

    for (let key in accountDict) {
        let account = accountDict[key];

        let indicator = document.createElement('li');
        indicator.setAttribute('data-bs-target', '#accounts');
        indicator.setAttribute('data-bs-slide-to', Object.keys(accountDict).indexOf(key));
        if (isFirst) {
            indicator.classList.add('active');
            isFirst = false;
        }
        carouselIndicators.appendChild(indicator);

        let item = document.createElement('div');
        item.classList.add('carousel-item');
        if (Object.keys(accountDict).indexOf(key) === 0) {
            item.classList.add('active');
        }

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

    // Refresh carousel if necessary
    let carousel = new bootstrap.Carousel(accounts);
}
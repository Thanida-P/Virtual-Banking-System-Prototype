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

        item.innerHTML = `
            <div class="account-info">
                <h5>${accountType}</h5>
                <p>Balance: &#3647;${account.balance}</p>
                <p>Account Number: ${account.accountNumber}</p>
            </div>
        `;

        carouselInner.appendChild(item);
    }

    // Refresh carousel
    carousel.refresh();
}
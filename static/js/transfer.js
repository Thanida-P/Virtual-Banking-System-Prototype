// document.addEventListener("DOMContentLoaded", function () {
//     // Add event listener to the form
//     const form = document.querySelector("form");
//     form.addEventListener("submit", function (event) {
//         if (!reviewTransfer()) {
//             event.preventDefault(); // Prevent form submission if validation fails
//         }
//     });
// });

// function reviewTransfer() {
//     // Get form elements
//     const fromAccount = document.querySelector("#owned_accounts .carousel-item.active");
//     const bank = document.querySelector("#bank").value;
//     const accountNumber = document.querySelector("#account_number").value;
//     const amount = document.querySelector("#amount").value;

//     // Check if all fields are filled
//     if (!fromAccount || !bank || !accountNumber || !amount) {
//         alert("Please fill in all fields.");
//     }

//     window.location.href = '/transfer/review';
// }
// var carousel = new bootstrap.Carousel('#owned_accounts', {
//     interval: false,
//     ride: false
// });

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
                <p>Account Number: ${account.accountNumber}</p>
            </div>
        `;

        carouselInner.appendChild(item);
    }
}

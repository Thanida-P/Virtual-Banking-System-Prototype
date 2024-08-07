document.addEventListener("DOMContentLoaded", function () {
    // Add event listener to the form
    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        if (!reviewTransfer()) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });
});

function reviewTransfer() {
    // Get form elements
    const fromAccount = document.querySelector("#owned_accounts .carousel-item.active");
    const bank = document.querySelector("#bank").value;
    const accountNumber = document.querySelector("#account_number").value;
    const amount = document.querySelector("#amount").value;

    // Check if all fields are filled
    if (!fromAccount || !bank || !accountNumber || !amount) {
        alert("Please fill in all fields.");
    }

    window.location.href = '/transfer/review';
}

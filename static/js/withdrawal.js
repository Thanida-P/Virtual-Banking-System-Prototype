$(document).ready(function() {
    // only for the withdrawal page
    $('#withdraw-form').on('submit', function(event) {
        const amount = $('#withdraw-amount').val();
        if (amount % 100 !== 0) {
            alert('Amount must be divisible by 100.');
            event.preventDefault();
        }
    });
});

var carousel = new bootstrap.Carousel('#owned_accounts', {
    interval: false,
    ride: false
});

function withdrawal() {
    const amount = $('#withdraw-amount').val();
    const phone = $('#phone-no').val();
    if (amount === '' || amount === '0' || phone === '') {
        alert('Please fill in all fields.');
    } else if (amount % 100 !== 0) {
        alert('Amount must be divisible by 100.');
    } else {
        window.location.href = '/withdraw/otp';
    }
}
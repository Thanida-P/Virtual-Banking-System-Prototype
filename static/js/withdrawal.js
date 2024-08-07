$(document).ready(function() {
    $('.carousel').carousel({
        interval: false // Disable automatic cycling
    });

    // only for the withdrawal page
    $('#withdraw-form').on('submit', function(event) {
        const amount = $('#withdraw-amount').val();
        if (amount % 100 !== 0) {
            alert('Amount must be divisible by 100.');
            event.preventDefault();
        }
    });
});

function reviewWithdrawal() {
    const amount = $('#withdraw-amount').val();
    if (amount === '' || amount === '0') {
        alert('Please enter an amount.');
    } else if (amount % 100 !== 0) {
        alert('Amount must be divisible by 100.');
    } else {
        window.location.href = '/withdraw/review';
    }
}
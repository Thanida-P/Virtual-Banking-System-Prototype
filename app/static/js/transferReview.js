cancel = true;

window.addEventListener('beforeunload', function (event) {
    if (cancel) {
        removeTransfer();
    }
});

function getTransactionId() {
    let url = window.location.href;
    let urlArray = url.split("/");
    let parameter = urlArray[urlArray.length - 1];
    let decodedParameter = atob(parameter);
    let transactionId = parseInt(decodedParameter.split("=")[1]);
    return transactionId;
}   

function confirmTransfer() {
    let transactionId = getTransactionId();
    fetch ("/confirmTransfer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            transactionId: transactionId
        })
    }).then(response => {
        if (response.ok) {
            cancel = false;
            alert("Transfer successful!");
            window.location.href = "/home";
        } else {
            alert("Transfer failed. Incorrect End-Account.");
            window.location.href = "/transfer";
        }
    });
}

function removeTransfer() {
    let transactionId = getTransactionId();
    fetch ("/removeTransfer", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            transactionId: transactionId
        })
    }).then(response => {
        if (response.ok) {
            window.location.href='/transfer';
        }
    });
}
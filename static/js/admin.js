function searchAccount() {
    var searchCitizenID = document.getElementsByName("searchCitizenID")[0].value;
    if (searchCitizenID === "") {
        alert("Please enter a Citizen ID");
        return;
    }

    fetch("/searchAccount", {
        method: "POST",
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `searchCitizenID=${searchCitizenID}`
    }).then((response) => {
            return response.json();
    }).then((data) => {
        if (data.status === "success") {
            document.getElementById("accountAvatar").innerHTML = '<img src="' + window.location.origin + '/static/' + data.filename + '" alt="avatar" class="rounded-circle img-fluid" style="width: 100px;" />';
        } 
    });

    
}
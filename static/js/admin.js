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
            document.getElementById("accountName").innerHTML = data.fullname;
            document.getElementById("accountUsername").innerHTML = data.username;
            document.getElementById("accountEmail").innerHTML = data.email;
            document.getElementById("accountCitizenID").innerHTML = data.citizenId;
            document.getElementById("accountPhno").innerHTML = data.phno;
            document.getElementById("accountMarital").innerHTML = data.marital;
            document.getElementById("accountEducation").innerHTML = data.education;
        } 
    });

    
}

function editAccount() {
    
}
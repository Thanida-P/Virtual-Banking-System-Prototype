var avatarDisplay;
var fullname;
var username;
var email;
var citizenId;
var phno;
var marital;
var education;

function searchAccount() {
  var searchCitizenID = document.getElementsByName("searchCitizenID")[0].value;
  if (searchCitizenID === "") {
    alert("Please enter a Citizen ID");
    return;
  }

  fetch("/searchAccount", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `searchCitizenID=${searchCitizenID}`,
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      if (data.status === "success") {
        avatarDisplay =
          '<img src="' +
          window.location.origin +
          "/static/" +
          data.filename +
          '" alt="avatar" class="rounded-circle img-fluid" style="width: 125px;" />';
        
        fullname = data.fullname;
        username = data.username;
        email = data.email;
        citizenId = data.citizenId;
        phno = data.phno;
        marital = data.marital;
        education = data.education;

        const modal = new bootstrap.Modal(
          document.getElementById("searchAccountModal"),
          {
            keyboard: false,
          }
        );
        modal.show();
      }

      //display
      document.getElementById("accountAvatar").innerHTML = avatarDisplay;
      document.getElementById("accountName").innerHTML = fullname;
      document.getElementById("accountUsername").innerHTML = username;
      document.getElementById("accountEmail").innerHTML = email;
      document.getElementById("accountCitizenID").innerHTML = citizenId;
      document.getElementById("accountPhno").innerHTML = phno;
      document.getElementById("accountMarital").innerHTML = marital;
      document.getElementById("accountEducation").innerHTML = education;

      //edit
      document.getElementById("fullname").value = fullname;
      document.getElementById("email").value = email;
      document.getElementById("phno").value = phno;
      document.getElementById("maritalstatus").value = marital.charAt(0).toLowerCase() + marital.slice(1);
      document.getElementById("citizenId").value = document.getElementById("citizenIdHidden").value = citizenId;
      
      var currentEducation = education.charAt(0).toLowerCase() + education.slice(1);
      if (currentEducation == "Prefer not to answer") {
        currentEducation = "unknown";
      }
    
      document.getElementById("education").value = currentEducation;
    });
}

function editAccount() {
    document.querySelectorAll(".editAccount").forEach(element => element.style.display = "flex");
    document.querySelectorAll(".showAccount").forEach(element => element.style.display = "none");
}

function cancelEditAccount() {
    document.querySelectorAll(".editAccount").forEach(element => element.style.display = "none");
    document.querySelectorAll(".showAccount").forEach(element => element.style.display = "flex");
}

function updateAccount() {
    form = document.getElementById("updateForm")
    const formData = new FormData(form);

    fetch('/updateAccount', {
        method: 'PUT',
        body: formData
    }).then(response => {
        if (response.ok) {
            alert('Account updated successfully!');
            location.reload();
        } else {
            alert('Failed to update account.');
        }
    }).catch(error => console.error('Error:', error));
}

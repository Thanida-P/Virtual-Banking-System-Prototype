document.addEventListener("DOMContentLoaded", function () {
  var inputSearchAccount = document.getElementById("searchCitizenID");
  inputSearchAccount.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("searchAccountBtn").click();
    }
  });

  var inputSearchBankAccount = document.getElementById("searchAccountNo");
  inputSearchBankAccount.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      document.getElementById("searchBankAccountBtn").click();
    }
  });
});

function searchBankAccount(){
  var searchAccountNo = document.getElementById("searchAccountNo").value;
  if (searchAccountNo === "") {
    alert("Please enter a Bank Account Number");
    return;
  }

  fetch("/searchAccount", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
  },
    body: JSON.stringify({ searchAccountNo: searchAccountNo }),
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
        bankAccounttype = data.bankAccounttype;
        bankId = data.bankId;
        banknumber = data.banknumber;
        balance = data.balance;

        const modal = new bootstrap.Modal(
          document.getElementById("searchBankModal"),
          {
            keyboard: false,
          }
        );
        modal.show();
      }

      //display
      document.getElementById("bankAccountAvatar").innerHTML = avatarDisplay;
      document.getElementById("bankAccountName").innerHTML = fullname;
      document.getElementById("bankAccountUsername").innerHTML = username;
      document.getElementById("bankAccountEmail").innerHTML = email;
      document.getElementById("bankAccountCitizenID").innerHTML = citizenId;
      document.getElementById("bankAccountPhno").innerHTML = phno;
      document.getElementById("bankAccountMarital").innerHTML = marital;
      document.getElementById("bankAccountEducation").innerHTML = education;
      document.getElementById("bankAccountType").innerHTML = bankAccounttype;
      document.getElementById("bankAccountBankId").innerHTML = bankId;
      document.getElementById("bankAccountNumber").innerHTML = banknumber;
      document.getElementById("bankAccountBalance").innerHTML = balance;
    })
}

function searchAccount() {
  var searchCitizenID = document.getElementById("searchCitizenID").value;
  if (searchCitizenID === "") {
    alert("Please enter a Citizen ID");
    return;
  }

  fetch("/searchAccount", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
  },
    body: JSON.stringify({ searchCitizenID: searchCitizenID }),
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
    form = document.getElementById("updateForm");
    const formData = new FormData(form);

    const formObject = {};
    formData.forEach((value, key) => {
        formObject[key] = value;
    });
    
    fetch('/updateAccount', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formObject)
       
    }).then(response => {
        if (response.ok) {
            alert('Account updated successfully!');
            location.reload();
        } else {
            alert('Failed to update account.');
        }
    }).catch(error => console.error('Error:', error));
}

function deleteBankAccount() {
    fetch('/deleteBankAccount', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ banknumber: bankId })
    }).then(response => {
        if (response.ok) {
            alert('Bank account deleted successfully!');
            location.reload();
        } else {
            alert('Failed to delete bank account.');
        }
    }).catch(error => console.error('Error:', error));
}
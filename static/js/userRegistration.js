const form = document.getElementById("userForm");
const userName = document.getElementById("userName");
const phoneNumber = document.getElementById("phoneNumber");
const email = document.getElementById("email");
const password = document.getElementById("password");
const buildingAssigned = document.getElementById("buildingAssigned");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  checkInputs();
});

function checkInputs() {
  // trim to remove the whitespaces
  const userNameValue = userName.value.trim();
  const phoneNumberValue = phoneNumber.value.trim();
  const emailValue = email.value.trim();
  const passwordValue = password.value.trim();
  const buildingAssignedValue = buildingAssigned.value.trim();

  if (userNameValue === "") {
    setErrorFor(userName, "User's Name cannot be blank");
  } else {
    setSuccessFor(userName);
  }
  if (phoneNumberValue === "") {
    setErrorFor(phoneNumber, "Phone Number cannot be blank");
  } else if (!isNumber(phoneNumberValue)) {
    setErrorFor(phoneNumber, "Not a valid number");
  } else {
    setSuccessFor(phoneNumber);
  }

  if (emailValue === "") {
    setErrorFor(email, "Email Id cannot be blank");
  } else if (!isEmail(emailValue)) {
    setErrorFor(email, "Not a valid email");
  } else {
    setSuccessFor(email);
  }
  if (passwordValue === "") {
    setErrorFor(password, "Password cannot be blank");
  } else if (passwordValue < 8) {
    setErrorFor(password, "Password Should be greater than 8");
  } else {
    setSuccessFor(password);
  }
  if (buildingAssignedValue === "") {
    setErrorFor(buildingAssigned, "Building Assigned cannot be blank");
  } else {
    setSuccessFor(buildingAssigned);
  }
}

function setErrorFor(input, message) {
  const formControl = input.parentElement;
  const small = formControl.querySelector("small");
  formControl.className = "input-field error";
  small.innerText = message;
}

function setSuccessFor(input) {
  const formControl = input.parentElement;
  formControl.className = "input-field success";
}

function isEmail(email) {
  return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
    email
  );
}

function isNumber(number) {
  var phoneno = /^\d{10}$/;
  if (number.match(phoneno)) {
    return true;
  } else {
    return false;
  }
}

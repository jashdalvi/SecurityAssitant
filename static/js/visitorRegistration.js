const form = document.getElementById("visitorForm");
const visitorName = document.getElementById("visitorName");
const visitorAddress = document.getElementById("visitorAddress");
const phoneNumber = document.getElementById("phoneNumber");
const visitorWork = document.getElementById("visitorWork");
const flatNo = document.getElementById("flatNo");

form.addEventListener("submit", (e) => {
  e.preventDefault();

  checkInputs();
});

function checkInputs() {
  // trim to remove the whitespaces
  const visitorNameValue = visitorName.value.trim();
  const visitorAddressValue = visitorAddress.value.trim();
  const phoneNumberValue = phoneNumber.value.trim();
  const visitorWorkValue = visitorWork.value.trim();
  const flatNoValue = flatNo.value.trim();

  if (visitorNameValue === "") {
    setErrorFor(visitorName, "Visitor Name cannot be blank");
  } else {
    setSuccessFor(visitorName);
  }

  if (visitorAddressValue === "") {
    setErrorFor(visitorAddress, "Address cannot be blank");
  } else {
    setSuccessFor(visitorAddress);
  }

  if (phoneNumberValue === "") {
    setErrorFor(phoneNumber, "Phone Number cannot be blank");
  } else if (!isNumber(phoneNumberValue)) {
    setErrorFor(phoneNumber, "Not a valid number");
  } else {
    setSuccessFor(phoneNumber);
  }

  if (visitorWorkValue === "") {
    setErrorFor(visitorWork, "Visitor's work cannot be blank");
  } else {
    setSuccessFor(visitorWork);
  }
  if (flatNoValue === "") {
    setErrorFor(flatNo, "Flat No to be Visited cannot be blank");
  } else {
    setSuccessFor(flatNo);
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

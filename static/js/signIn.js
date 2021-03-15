const user_login_btn = document.querySelector("#user-login-btn");
const admin_login_btn = document.querySelector("#admin-login-btn");

const container = document.querySelector(".container");

admin_login_btn.addEventListener("click", () => {
  container.classList.add("admin-mode");
});

user_login_btn.addEventListener("click", () => {
  container.classList.remove("admin-mode");
});
// Functions for showing message
// function setErrorFor(input, message) {
//   const formControl = input.parentElement;
//   const small = formControl.querySelector("small");
//   formControl.className = "input-field error";
//   small.innerText = message;
// }

// function setSuccessFor(input) {
//   const formControl = input.parentElement;
//   formControl.className = "input-field success";
// }

// function isEmail(email) {
//   return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(
//     email
//   );
// }

// Validate User Login Form
// const userLoginForm = document.getElementById("userLoginForm");
// const userEmail = document.getElementById("userEmail");
// const userPassword = document.getElementById("userPassword");

// userLoginForm.addEventListener("submit", (e) => {
//    e.preventDefault();

//   checkUserLoginInputs();
// });

// function checkUserLoginInputs() {
//   // trim to remove the whitespaces
//   const userEmailValue = userEmail.value.trim();
//   const userPasswordValue = userPassword.value.trim();

//   if (userEmailValue === "") {
//     setErrorFor(userEmail, "Email Id cannot be blank");
//   } else if (!isEmail(userEmailValue)) {
//     setErrorFor(userEmail, "Not a valid email");
//   } else {
//     setSuccessFor(userEmail);
//   }
//   if (userPasswordValue === "") {
//     setErrorFor(userPassword, "Password cannot be blank");
//   } else {
//     setSuccessFor(userPassword);
//   }
// }

// Validate Admin Login
// const adminLoginForm = document.getElementById("adminLoginForm");
// const adminEmail = document.getElementById("adminEmail");
// const adminPassword = document.getElementById("adminPassword");

// adminLoginForm.addEventListener("submit", (e) => {
//   e.preventDefault();

//   checkAdminLoginInputs();
//   window.location.href("adminDashboard.html");
// });

// function checkAdminLoginInputs() {
//   // trim to remove the whitespaces
//   const adminEmailValue = adminEmail.value.trim();
//   const adminPasswordValue = adminPassword.value.trim();

//   if (adminEmailValue === "") {
//     setErrorFor(adminEmail, "Email Id cannot be blank");
//   } else if (!isEmail(adminEmailValue)) {
//     setErrorFor(adminEmail, "Not a valid email");
//   } else {
//     setSuccessFor(adminEmail);
//   }
//   if (adminPasswordValue === "") {
//     setErrorFor(adminPassword, "Password cannot be blank");
//   } else {
//     setSuccessFor(adminPassword);
//   }
// }

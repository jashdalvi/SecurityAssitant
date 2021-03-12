// Show navbar
const showNavbar = (toggleId, navId, bodyId, headerId) => {
  const toggle = document.getElementById(toggleId);
  const nav = document.getElementById(navId);
  const bodyDesktop = document.getElementById(bodyId);
  const headerDesktop = document.getElementById(headerId);
  //validate that all variable exists
  if (toggle && nav && bodyId && headerId) {
    toggle.addEventListener("click", () => {
      //show navbar
      nav.classList.toggle("show");
      // change icon to cancel
      toggle.classList.toggle("bx-x");
      // add padding to body and header for large screen
      bodyDesktop.classList.toggle("body-desktop");
      headerDesktop.classList.toggle("body-desktop");
    });
  }
};

showNavbar("header-toggle", "side_bar", "body-desktop", "header-desktop");

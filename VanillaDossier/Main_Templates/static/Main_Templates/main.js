// this could be refactored::

// navbar animation, just adding a css class to it on click
// need to have this function on the actual html/css properties since
// it needs to be an onClick() function

let htmlDoc = document.getElementById("html_id");
let colorToggle = document.getElementById("js_color_scheme_toggle");
let mainNav = document.getElementById("js_menu");
let navBarToggle = document.getElementById("js_navbar_toggle");



// Color scheme toggle mode
function darkLightModesSwitch(htmlDoc) {
  htmlDoc.classList.toggle("dark_mode");
}

colorToggle.addEventListener("click", function() {
  htmlDoc.classList.toggle("dark_mode");
});

function hamburgerAnimation(mainNav) {
  mainNav.classList.toggle("change_hamburger");
}

// this needs to be done separately, by the ID while the hamburgerAnimation is done by onClick
navBarToggle.addEventListener("click", function() {
  // mainNav.classList.toggle('change_hamburger');
  mainNav.classList.toggle("active_navbar");
});

// free rides to the top

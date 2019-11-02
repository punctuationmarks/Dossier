let bodyElement = document.getElementById("body_id");
let colorToggleButon = document.getElementById("color_scheme_toggle_button");
let mainNav = document.getElementById("navbar_menu");
let navBarToggleButton = document.getElementById("navbar_toggle_button");

function hamburgerAnimation(mainNav) {
  mainNav.classList.toggle("change_hamburger");
}

// this needs to be done separately, by the ID while the hamburgerAnimation is done by onClick
navBarToggleButton.addEventListener("click", function() {
  // mainNav.classList.toggle('change_hamburger');
  mainNav.classList.toggle("active_navbar");
});

// Color scheme toggle mode

// okay so this "works", meaning it keeps the settings, buuuttt
// there is a point where it glitches and it shows the other class while loading next page
// work around is having the page start with both classes, then removing them based on localStorage
// and the button (once clicked). that needs to be refactored

// What to do when localStorage is X
switch (window.localStorage.getItem("color_theme")) {
  case "light":
    bodyElement.classList.remove("dark_mode");
    bodyElement.classList.add("light_mode");
    break;

  case "dark":
    bodyElement.classList.remove("light_mode");
    bodyElement.classList.add("dark_mode");
    break;

  case undefined:
    bodyElement.classList.remove("dark_mode");
    bodyElement.classList.add("light_mode");
    break;
  default:
    bodyElement.classList.remove("dark_mode");
    bodyElement.classList.add("light_mode");
    break;
}

// Altering the localStorage and the class list (this is to make it immediate, instead of on reload)
colorToggleButon.addEventListener("click", function() {
  switch (window.localStorage.getItem("color_theme")) {
    case "light":
      window.localStorage.setItem("color_theme", "dark");
      bodyElement.classList.remove("light_mode");
      bodyElement.classList.add("dark_mode");
      break;
    case "dark":
      window.localStorage.setItem("color_theme", "light");
      bodyElement.classList.remove("dark_mode");
      bodyElement.classList.add("light_mode");
      break;
    case undefined:
      window.localStorage.setItem("color_theme", "light");
      bodyElement.classList.add("light_mode");
    default:
      window.localStorage.setItem("color_theme", "light");
      bodyElement.classList.add("light_mode");
  }
});

// TO BUILD!
// free rides to the top

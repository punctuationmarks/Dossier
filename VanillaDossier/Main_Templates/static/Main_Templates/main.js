let bodyElement = document.getElementById("body_id");
let colorToggleButon = document.getElementById("color_scheme_toggle_button");
let navbarMenu = document.getElementById("navbar_menu");
let navBarToggleButton = document.getElementById("navbar_toggle_button");
let navBarImage = document.getElementById("nav_bar");
let footerImage = document.getElementById("quick_buttons_ul");

function hamburgerAnimation(navbarMenu) {
  navbarMenu.classList.toggle("change_hamburger");
}

// this needs to be done separately, by the ID while the hamburgerAnimation is done by onClick
navBarToggleButton.addEventListener("click", function() {
  navbarMenu.classList.toggle("nav_ul");
  navbarMenu.classList.toggle("active_navbar");
});

let screen_size = window.innerWidth * window.innerHeight;
console.log("Inner height :" + window.innerHeight);
console.log("Inner Width :" + window.innerWidth);

console.log("Product = " + screen_size);

// What to do when localStorage is X
switch (window.localStorage.getItem("color_theme")) {
  case "light":
    bodyElement.classList.remove("dark_mode");
    navBarImage.classList.remove("dark_image");
    footerImage.classList.remove("footer_dark_image");
    bodyElement.classList.add("light_mode");
    navBarImage.classList.add("light_image");
    footerImage.classList.add("footer_light_image");
    break;

  case "dark":
    bodyElement.classList.remove("light_mode");
    navBarImage.classList.remove("light_image");
    footerImage.classList.remove("footer_light_image");
    bodyElement.classList.add("dark_mode");
    navBarImage.classList.add("dark_image");
    footerImage.classList.add("footer_dark_image");
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
      navBarImage.classList.remove("light_image");
      footerImage.classList.remove("footer_light_image");
      bodyElement.classList.add("dark_mode");
      navBarImage.classList.add("dark_image");
      footerImage.classList.add("footer_dark_image");
      break;
    case "dark":
      window.localStorage.setItem("color_theme", "light");
      bodyElement.classList.remove("dark_mode");
      navBarImage.classList.remove("dark_image");
      footerImage.classList.remove("footer_dark_image");
      bodyElement.classList.add("light_mode");
      navBarImage.classList.add("light_image");
      footerImage.classList.add("footer_light_image");
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

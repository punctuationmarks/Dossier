let bodyElement = document.getElementById("body_id");
let colorToggleButtonNavbar = document.getElementById("color_scheme_toggle_button_navbar");
let colorToggleButtonFooter = document.getElementById("color_scheme_toggle_footer");
let navbarMenu = document.getElementById("navbar_menu");
let footerToggleButton = document.getElementById("footer_toggle_activator");
let navBarImage = document.getElementById("header_section");
let quickButtons = document.getElementById("quick_buttons_ul");


footerToggleButton.addEventListener("click", function() {
  // double delay here for the slowness added to the fade out, CSS does not provide
  // a smoother fade out transition that I am aware of
  const delay = 200; //miliseconds

  setTimeout(function() {
    quickButtons.classList.toggle("footer_ul");
    quickButtons.classList.toggle("active_footer");
  }, delay);
});

// What to do when localStorage is X
switch (window.localStorage.getItem("color_theme")) {
  case "light":
    bodyElement.classList.remove("dark_mode");
    navBarImage.classList.remove("dark_image");
    quickButtons.classList.remove("footer_dark_image");
    bodyElement.classList.add("light_mode");
    navBarImage.classList.add("light_image");
    quickButtons.classList.add("footer_light_image");
    break;

  case "dark":
    bodyElement.classList.remove("light_mode");
    navBarImage.classList.remove("light_image");
    quickButtons.classList.remove("footer_light_image");
    bodyElement.classList.add("dark_mode");
    navBarImage.classList.add("dark_image");
    quickButtons.classList.add("footer_dark_image");
    break;

  case undefined:
    bodyElement.classList.remove("dark_mode");
    navBarImage.classList.remove("dark_image");
    quickButtons.classList.remove("footer_dark_image");
    bodyElement.classList.add("light_mode");
    navBarImage.classList.add("light_image");
    quickButtons.classList.add("footer_light_image");
    break;
  default:
    bodyElement.classList.remove("dark_mode");
    navBarImage.classList.remove("dark_image");
    quickButtons.classList.remove("footer_dark_image");
    bodyElement.classList.add("light_mode");
    navBarImage.classList.add("light_image");
    quickButtons.classList.add("footer_light_image");
    break;
}

// Altering the localStorage and the class list (this is to make it immediate, instead of on reload)
colorToggleButtonNavbar.addEventListener("click", function() {
  const delay = 150; //miliseconds
  switch (window.localStorage.getItem("color_theme")) {
    case "light":
    setTimeout(function() {
      window.localStorage.setItem("color_theme", "dark");
      bodyElement.classList.remove("light_mode");
      navBarImage.classList.remove("light_image");
      quickButtons.classList.remove("footer_light_image");
      bodyElement.classList.add("dark_mode");
      navBarImage.classList.add("dark_image");
      quickButtons.classList.add("footer_dark_image");
    }, delay);

      break;

      case "dark":
      setTimeout(function() {
      window.localStorage.setItem("color_theme", "light");
      bodyElement.classList.remove("dark_mode");
      navBarImage.classList.remove("dark_image");
      quickButtons.classList.remove("footer_dark_image");
      bodyElement.classList.add("light_mode");
      navBarImage.classList.add("light_image");
      quickButtons.classList.add("footer_light_image");
    }, delay);
      break;
    // case undefined:
    //   window.localStorage.setItem("color_theme", "light");
    //   bodyElement.classList.add("light_mode");
    default:
      window.localStorage.setItem("color_theme", "light");
      bodyElement.classList.add("light_mode");
  }
});

colorToggleButtonFooter.addEventListener("click", function() {
  switch (window.localStorage.getItem("color_theme")) {
    case "light":
      window.localStorage.setItem("color_theme", "dark");
      bodyElement.classList.remove("light_mode");
      navBarImage.classList.remove("light_image");
      quickButtons.classList.remove("footer_light_image");
      bodyElement.classList.add("dark_mode");
      navBarImage.classList.add("dark_image");
      quickButtons.classList.add("footer_dark_image");
      break;
    case "dark":
      window.localStorage.setItem("color_theme", "light");
      bodyElement.classList.remove("dark_mode");
      navBarImage.classList.remove("dark_image");
      quickButtons.classList.remove("footer_dark_image");
      bodyElement.classList.add("light_mode");
      navBarImage.classList.add("light_image");
      quickButtons.classList.add("footer_light_image");
      break;
    // case undefined:
    //   window.localStorage.setItem("color_theme", "light");
    //   bodyElement.classList.add("light_mode");
    default:
      window.localStorage.setItem("color_theme", "light");
      bodyElement.classList.add("light_mode");
  }
});

// for testing screen sizes
let screen_size = window.innerWidth * window.innerHeight;
console.log("Inner height :" + window.innerHeight);
console.log("Inner Width :" + window.innerWidth);

console.log("Product = " + screen_size);

// TO BUILD!
// free rides to the top

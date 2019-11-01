// this could be refactored::

// navbar animation, just adding a css class to it on click
// need to have this function on the actual html/css properties since
// it needs to be an onClick() function

let bodyElement = document.getElementById("body_id");
let colorToggle = document.getElementById("js_color_scheme_toggle");
let mainNav = document.getElementById("js_menu");
let navBarToggle = document.getElementById("js_navbar_toggle");

// // Color scheme toggle mode
// function darkLightModesSwitch(bodyElement) {
//   bodyElement.classList.toggle("dark_mode");
// }
//
// colorToggle.addEventListener("click", function() {
//   bodyElement.classList.toggle("dark_mode");
// });

function hamburgerAnimation(mainNav) {
  mainNav.classList.toggle("change_hamburger");
}

// this needs to be done separately, by the ID while the hamburgerAnimation is done by onClick
navBarToggle.addEventListener("click", function() {
  // mainNav.classList.toggle('change_hamburger');
  mainNav.classList.toggle("active_navbar");
});


// read into this:
// https://blog.logrocket.com/the-complete-guide-to-using-localstorage-in-javascript-apps-ba44edb53a36/
// this also looks like a more broad stroke:
// https://blog.logrocket.com/beyond-cookies-todays-options-for-client-side-data-storage/

// Color scheme toggle mode
function darkLightModesSwitch(bodyElement) {
  bodyElement.classList.toggle("dark_mode");
}


// these log fine, but doesn't allow reversing, perhaps a switch statement would be best?
colorToggle.addEventListener("click", function() {
  if (window.localStorage.getItem("color_theme")) {
    window.localStorage.setItem("color_theme", "light_mode");
    console.log(window.localStorage.getItem("color_theme"));
  } else {
    window.localStorage.setItem("color_theme", "dark_mode");
    console.log(window.localStorage.getItem("color_theme"));
  }
});

// TO BUILD!
// free rides to the top

// // Mario says to not use cookies:

//
// // Testing Cookies for holding the theme in state
//
// function setCookie(cname, cvalue, exdays) {
//   var d = new Date();
//   d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
//   var expires = "expires=" + d.toGMTString();
//   document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
// }
//
// function getCookie(cname) {
//   var name = cname + "=";
//   var decodedCookie = decodeURIComponent(document.cookie);
//   var ca = decodedCookie.split(";");
//   for (var i = 0; i < ca.length; i++) {
//     var c = ca[i];
//     while (c.charAt(0) == " ") {
//       c = c.substring(1);
//     }
//     if (c.indexOf(name) == 0) {
//       return c.substring(name.length, c.length);
//     }
//   }
//   return "";
// }

// // W3 schools example
// function checkCookie() {
//   var user = getCookie("username");
//   if (user != "") {
//     alert("Welcome again " + user);
//   } else {
//     user = prompt("Please enter your name:", "");
//     if (user != "" && user != null) {
//       setCookie("username", user, 30);
//     }
//   }
// }

// colorToggle.addEventListener("click", function() {
//   if (getCookie("theme_cookie").length > 0) {
//     setCookie("theme_cookie", "dark_cookie", 17);
//     console.log(getCookie("theme_cookie") + " dark theme cookie active");
//   } else {
//     setCookie("theme_cookie", "light_cookie", 17);
//     console.log(getCookie("theme_cookie") + " ligth theme cookie active");
//   }
// });

// this could be refactored::

// navbar animation, just adding a css class to it on click
// need to have this function on the actual html/css properties since
// it needs to be an onClick() function

let mainNav = document.getElementById('js_menu');
let navBarToggle = document.getElementById('js_navbar_toggle');


function hamburgerAnimation(mainNav) {
    mainNav.classList.toggle("change_hamburger");
}


// this needs to be done separately, by the ID while the hamburgerAnimation is done by onClick
navBarToggle.addEventListener('click', function() {
    // mainNav.classList.toggle('change_hamburger');
    mainNav.classList.toggle('active_navbar');
});


// free rides to the top

https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog

have the css be universal, meaning keep it on the root html tags
and then cascade when necessary. currently you're drilling too deep, which 
means you'll be doing too much repetitive code, or it'll look less 
uniform


layout is looking better but the UI is still ugly, as fuck

- next, finish all the sever side stuff with the basics for the app
so you can beta test it on your pone before you get too deep into the
css



ideas: make it vanilla EVERYTHING, so no bootstrap and just vanilla JS (you need to get better at it anyway)
thought: make it on heroku and allow people to sign up (with a secret key?)
could make it super easy to change and make into a cyclist forum too
https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog/13-Deployment-Heroku/django_project

- Having two separate CRUD apps that are essentially the same
  but different only for the user
  (need to make sure "Thoughts" and "WorkIdeas" are visually different enough)


- need to fix the navbar links, make it look more smooth? idk, something that is more universal when it comes to
mobile (mostly) and some desktop. (maybe have the navbar links in line?)

following, loosely this: https://itnext.io/how-to-build-a-responsive-navbar-using-flexbox-and-javascript-eb0af24f19bf


navbar:
https://www.quanzhanketang.com/css/css_navbar.html
https://www.w3schools.com/howto/howto_js_navbar_sticky.asp
https://www.w3schools.com/html/html_responsive.asp
https://www.w3schools.com/Css/css_navbar.asp





- need to have responsive page, flex box most likely, have a dark theme (or make it default?)
- extremely assessible



NEEDED:
service workers, especially with the free heroku app

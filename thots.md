
the quick link buttons have ISSUES
the search bar with the POST button isn't aligning correctly
(tried flex and grid and it's not working, need research)


The color scheme does not stay permanent, lookig into cookies for this

The new cooler looking button is on the different branch, needs small polishing

Javscript is written mostly in ES5, needs to be refactored into ES6 (plus you'll get to learn the bigger differences)


https://github.com/CoreyMSchafer/code_snippets/tree/master/Django_Blog

have the css be universal, meaning keep it on the root html tags
and then cascade when necessary. currently you're drilling too deep, which
means you'll be doing too much repetitive code, or it'll look less
uniform

### ISSUES ####
# SO WE CAN;T HAVE THE TIMEON THE BASE.HTML PAGE, SO IT STILL only
# RENDERS ON THE HOME PAGE (HOW IT'S CURRENTLY WRITTEN THROUGH CONTEXT)
# IN THE Main_Templates/views


layout is looking better but the UI is still ugly, as fuck

- next, finish all the sever side stuff with the basics for the app
so you can beta test it on your pone before you get too deep into the
css



### COMING UP NOW! ####
# NEEDS TO BE THROWN ON AN ACTUAL DEPLOY FOR FIELD TESTING
# BUT BEFOREHAND, NEED TO HAVE CSV FILE UPLOAD/DOWNLOAD (AT LEAST DOWNLOAD)



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

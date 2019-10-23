from django.shortcuts import render
from datetime import datetime
# thoughts on having a user greeting? not sure I want it, eh.
# but haven't built one here before so might be interesting

# HAVE SOME QUICKPEAKS INTO WHAT'S AVAIABLE ON THE DATABASE FROM THE HOME SCREEN?

# from django.contrib.auth.models import User




# BROKE SOMETHING WITH THE GRID LAYOUT, EVERYTHING IN THE MAIN IS SQUISHY

def home(request):
    # NEED TO DOUBLE CHECK HOW TO COVERT THIS TO UTC DATETIME,
    # SINCE THIS CODE WILL BE ON THE SERVER AND WHEREVER THE PERSON'S SERVER
    # IS LOCATED WILL BE WHERE THE DATE WILL BE (ISSUE IF THEY USE THEIR OWN SERVER?)
    # ORMAYBE
    current_date = datetime.today().strftime('%Y-%m-%d')
    context = {'current_time' : current_date}
    return render(request, 'Main_Templates/home.html', context)

def about(request):
    return render(request, 'Main_Templates/about.html')

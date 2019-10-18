from django.shortcuts import render
from datetime import datetime
from pytz import utc
# thoughts on having a user greeting? not sure I want it, eh.
# but haven't built one here before so might be interesting
# from django.contrib.auth.models import User







def home(request):
    current_utc = utc.localize(datetime.utcnow())
    context = {'current_time' : current_utc}
    return render(request, 'Main_Templates/home.html', context)

def about(request):
    return render(request, 'Main_Templates/about.html')

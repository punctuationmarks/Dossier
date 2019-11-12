# uploading a csv file for the database
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from datetime import datetime
import csv, io
from Dossiers.models import DossiersModel
from Thoughts.models import ThoughtsModel
from Ideas.models import IdeasModel



# ISSEUS:
# TIME IS THE ISSUE SEE HOW IT'S SOLVED IN THE PREVIOUS BETA version

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




###
### WORKING ON MAKING THE UPLOAD CAPABILITY. ###
### FEATURES TO ADD:
## might be nice to have a button for not having headers
## might be nice to have a drop down on different types of files
## might be nice to have a way to see the entire database aferwards?
## ## before even committing the changes

# since this will only be used and built by the individual user
# allowing only the superuser to upload csv files
# this is what is passed to the decorators
@permission_required('admin/can_add_log_entry')
def upload_csv_dossier(request):
    template = "Main_Templates/upload_csv.html"

    # will be displayed to ensure the user knows what
    # the csv file will require
    prompt = {
        'order' : 'Order of the .csv file should be as follows: \
                    NAME, HOBBIES, WORK, APPEARANCE, notable_memories, DISCUSSIONS\
                    * The headers are needed\
                    * The posted times will default to current, you can alter this in admin\
                    * User is forced as the Super User, do not declare user'
    }

    if request.method == "GET":
        return render(request, template, prompt)

    # forcing the upload to be csv, even though .xcl or even .txt would work
    # this is just because I don't want users not knowing how to properly upload
    # a database file just willy nilly uploading shit
    user_uploaded_file = request.FILES['file']

    if not user_uploaded_file.endswith('.csv'):
        messages.error(request, "Needs to be a .csv file, change this if you want")

    csv_db = user_uploaded_file.read().decode('utf-8')

    # converting the cs file to a string for upload
    db_as_io_string = io.StringIO(csv_db)

    # skipping the header
    next(db_as_io_string)

    # forcing the user to be the super user
    # this is only for the opensource version,
    # it'd be fairly easy to make this looser, with just having
    # a check for the logged in user to be the only user to upload,
    # but I feel this is a tad more secure if there is any vulnerabilities
    explicit_super_user = User.objects.first()

    # why are we using a csv.reader if we're reading this as a string?
    for col in csv.reader(db_as_io_string):
        # dropping the update, keeping the create
        _, created = DossiersModel.objects.update_or_create(
            name = col[0],
            hobbies = col[1],
            work = col[2],
            appearance = col[3],
            notable_memories = col[4],
            discussions = col[5],
            author = explicit_super_user
        )
    context = {}

    return render(request, template, context)


@permission_required('admin/can_add_log_entry')
def upload_csv_thoughts(request):
    template = "Main_Templates/upload_csv.html"

    # will be displayed to ensure the user knows what
    # the csv file will require
    prompt = {
        'order' : 'Order of the .csv file should be as follows: \
                    Title, body\
                    * The headers are needed\
                    * The posted times will default to current, you can alter this in admin\
                    * User is forced as the Super User, do not declare user'
    }


    if request.method == "GET":
        return render(request, template, prompt)

    # forcing the upload to be csv, even though .xcl or even .txt would work
    # this is just because I don't want users not knowing how to properly upload
    # a database file just willy nilly uploading shit
    user_uploaded_file = request.FILES['file']
    #
    # if not user_uploaded_file.endswith('.csv'):
    #     messages.error(request, "Needs to be a .csv file, change this feature if you want")

    csv_db = user_uploaded_file.read().decode('utf-8')

    # converting the cs file to a string for upload
    db_as_io_string = io.StringIO(csv_db)

    # skipping the header
    next(db_as_io_string)

    # forcing the user to be the super user
    # this is only for the opensource version,
    # it'd be fairly easy to make this looser, with just having
    # a check for the logged in user to be the only user to upload,
    # but I feel this is a tad more secure if there is any vulnerabilities
    explicit_super_user = User.objects.first()

    # why are we using a csv.reader if we're reading this as a string?
    for col in csv.reader(db_as_io_string, delimiter = "|"):
        # dropping the update, keeping the create
        _, created = ThoughtsModel.objects.update_or_create(
            title = col[0],
            body = col[1],
            date_originally_posted = datetime.today().strftime('%Y-%m-%d'),
            author = explicit_super_user
        )
    context = {}

    return render(request, template, context)



@permission_required('admin/can_add_log_entry')
def upload_csv_ideas(request):
    template = "Main_Templates/upload_csv.html"

    # will be displayed to ensure the user knows what
    # the csv file will require
    prompt = {
        'order' : 'Order of the .csv file should be as follows: \
                    Title, body\
                    * The headers are needed\
                    * The posted times will default to current, you can alter this in admin\
                    * User is forced as the Super User, do not declare user'
    }


    if request.method == "GET":
        return render(request, template, prompt)

    # forcing the upload to be csv, even though .xcl or even .txt would work
    # this is just because I don't want users not knowing how to properly upload
    # a database file just willy nilly uploading shit
    user_uploaded_file = request.FILES['file']
    #
    # if not user_uploaded_file.endswith('.csv'):
    #     messages.error(request, "Needs to be a .csv file, change this feature if you want")

    csv_db = user_uploaded_file.read().decode('utf-8')

    # converting the cs file to a string for upload
    db_as_io_string = io.StringIO(csv_db)

    # skipping the header
    next(db_as_io_string)

    # forcing the user to be the super user
    # this is only for the opensource version,
    # it'd be fairly easy to make this looser, with just having
    # a check for the logged in user to be the only user to upload,
    # but I feel this is a tad more secure if there is any vulnerabilities
    explicit_super_user = User.objects.first()

    # why are we using a csv.reader if we're reading this as a string?
    for col in csv.reader(db_as_io_string, delimiter = "|"):
        # dropping the update, keeping the create
        _, created = ThoughtsModel.objects.update_or_create(
            title = col[0],
            body = col[1],
            date_originally_posted = datetime.today().strftime('%Y-%m-%d'),
            author = explicit_super_user
        )
    context = {}

    return render(request, template, context)

from django.shortcuts import render

# uploading a csv file for the database
import csv, io
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

from Dossiers.models import DossiersModel
from Thoughts.models import ThoughtsModel
from WorkIdeas.models import WorkIdeasModel

from datetime import datetime


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
### WORKING ON MAKING THE UPLOAD CAPABILITY. THESE ARE NOT CONNECTED JUST YET ###


# Following this concept:
# https://github.com/punctuationmarks/Dossiers-and-Notes-Private-Django-Project-/search?q=csv&unscoped_q=csv

# allowing admin/super_user to upload CSV files to database
# @permission_required('admin/can_add_log_entry')
# def dossier_upload_csv_file(request):
#     template = "main/upload_csv_file.html"
#     # displaying this to ensure the user knows what's in the csv file
#     prompt = {
#         'order': "Order of csv should be name, hobbies, appearance, discussions. \
#                     User is forced to be the Super User, do not declare"
#     }
#
#
#     if request.method == "GET":
#          return render(request, template, prompt)
#
#     # checking to make sure the file uploaded is .csv
#     csv_file = request.FILES['file']
#
#     if not csv_file.name.endswith('.csv'):
#         messages.error(request, "Needs to be a CSV file")
#
#     csv_dataset = csv_file.read().decode('utf-8')
#     # converting the csv file to a string
#     io_string = io.StringIO(csv_dataset)
#     # skipping the header
#     next(io_string)
#
#     # declairing the user to be the default Super User
#     super_user = User.objects.first()
#
#     for column in csv.reader(io_string):
#         # nice little trick to save the data to database without
#         # having to call .save()
#         _, created = DossierPost.objects.update_or_create(
#                 name = column[0],
#                 hobbies = column[1],
#                 appearance = column[2],
#                 discussions = column[3],
#                 author = super_user
#         )
#
#     context = {}
#
#     return render(request, template, context)
#
#
#
# # declaring writing prompt for both blog and notes (since identical)
# writing_prompt_for_blog_n_thots = {
#     'order': "Order of csv should be title, body \
#                 User is forced to be the Super User, do not declare"
# }
#
# # allowing admin/super_user to upload CSV files to database
# @permission_required('admin/can_add_log_entry')
# def blog_upload_csv_file(request):
#     template = "main/upload_csv_file.html"
#     # displaying this to ensure the user knows what's in the csv file
#     prompt = writing_prompt_for_blog_n_thots
#
#
#     if request.method == "GET":
#          return render(request, template, prompt)
#
#     # checking to make sure the file uploaded is .csv
#     csv_file = request.FILES['file']
#
#     if not csv_file.name.endswith('.csv'):
#         messages.error(request, "Needs to be a CSV file")
#
#     csv_dataset = csv_file.read().decode('utf-8')
#     # converting the csv file to a string
#     io_string = io.StringIO(csv_dataset)
#     # skipping the header
#     next(io_string)
#
#     # declairing the user to be the default Super User
#     super_user = User.objects.first()
#
#     for column in csv.reader(io_string):
#         # nice little trick to save the data to database without
#         # having to call .save()
#         _, created = BlogPost.objects.update_or_create(
#                 title = column[0],
#                 body = column[1],
#                 author = super_user
#         )
#
#     context = {}
#
#     return render(request, template, context)
#
#
#
# # allowing admin/super_user to upload CSV files to database
# @permission_required('admin/can_add_log_entry')
# def codingThots_upload_csv_file(request):
#     template = "main/upload_csv_file.html"
#     # displaying this to ensure the user knows what's in the csv file
#     prompt = writing_prompt_for_blog_n_thots
#
#     if request.method == "GET":
#          return render(request, template, prompt)
#
#     # checking to make sure the file uploaded is .csv
#     csv_file = request.FILES['file']
#
#     if not csv_file.name.endswith('.csv'):
#         messages.error(request, "Needs to be a CSV file")
#
#     csv_dataset = csv_file.read().decode('utf-8')
#     # converting the csv file to a string
#     io_string = io.StringIO(csv_dataset)
#     # skipping the header
#     next(io_string)
#
#     # declairing the user to be the default Super User
#     super_user = User.objects.first()
#
#     for column in csv.reader(io_string):
#         # nice little trick to save the data to database without
#         # having to call .save()
#         _, created = CodingThotsPost.objects.update_or_create(
#                 title = column[0],
#                 body = column[1],
#                 author = super_user
#         )
#
#     context = {}
#
#     return render(request, template, context)

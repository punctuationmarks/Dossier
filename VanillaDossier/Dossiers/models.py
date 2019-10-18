from django.db import models  # needed to user ORM
from django.utils import timezone  # for time data for post
from django.contrib.auth.models import User  # tieing the user to the post
from django.urls import reverse
from django.contrib import admin  # for admin view


class DossiersModel(models.Model):
    name = models.CharField(max_length=100)
    hobbies = models.CharField(max_length=300, blank=True)
    work = models.CharField(max_length=300, blank=True)
    appearance = models.CharField(max_length=100, blank=True)
    # field for specificities, like roommates' or cat's names
    toRemember = models.CharField(max_length=100, blank=True)
    discussions = models.TextField(blank=True)
    date_originally_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"""{self.name}, {self.date_originally_posted}"""

    # direct url for routing, based on primary key
    def get_absolute_url(self):
        return reverse('dossiers-post-detail', kwargs={'pk': self.pk})


class DossiersAdmin(admin.ModelAdmin):
    actions = ['download_csv_file']
    list_display = ('name', 'hobbies', 'work', 'appearance',
                    'toRemember', 'discussions', 'date_originally_posted')

    def download_csv_file(self, request, queryset):
        # cool thing about Python is importing inside a function
        # inside of an OOP class, interesting stuff
        import csv
        from django.http import HttpResponse
        from io import StringIO
        import time

        # adding a time stamp to the csv file name
        # so user can download same file multiple times
        time_stamp = time.strftime("%Y%m%d%H%M")

        # allowing the writing the string as a file
        # with StringIO
        file = StringIO()

        # initializing the writer
        writer = csv.writer(file)

        # writing the headers
        writer.writerow['name', 'hobbies', 'work', 'appearance',
                        'toRemember', 'discussions', 'date_originally_posted']

        # allowing the user to select what they want written in their
        # Django default of "selected_set"
        # csv file, looping over that and writing each row
        for selected_set in queryset:
            writer.writerow([selected_set.name,
                             selected_set.hobbies,
                             selected_set.work,
                             selected_set.appearance,
                             selected_set.toRemember,
                             selected_set.discussions,
                             selected_set.date_originally_posted])

        # settng the cursor at the beginning of the file after writing
        file.seek(0)

        response = HttpResponse(file, content_type="text/csv")

        # allowing the downloading as an attachment, and file name default
        # more info on Content-Disposition
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition
        response['Content-Disposition'] = f'''attachement; filename=dossiers_{time_stamp}.csv'''
        return response

    # making the download csv file more pleasing
    download_csv_file.short_description = "Download a .csv file for what's selected"

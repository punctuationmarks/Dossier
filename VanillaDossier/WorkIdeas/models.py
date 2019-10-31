# allowing the structure of the model to fit the ORM
from django.db import models
# used for keeping track of the time for the post
from django.utils import timezone
# tieing the post to the correct user
from django.contrib.auth.models import User
# for a "slug", a url based on the post's primary key
from django.urls import reverse
# being able to customize how the backend looks:
from django.contrib import admin


class WorkIdeasModel(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    # date that can be updated
    date_posted = models.DateTimeField(default=timezone.now)
    # this will update the time, every time a post is updated
    last_modified = models.DateTimeField(auto_now=True)
    # sets the datetime only to when the post is originally created,
    # you can never update the date posted argument
    date_originally_posted = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # this is done so that once a post is created, the user
    # is redirected directly to that detailed view
    def get_absolute_url(self):
        return reverse('workIdeas-post-detail', kwargs={'pk':self.pk})

# how the data is shown on the backend,
# also affects how the csv is dispayed
class WorkIdeasAdmin(admin.ModelAdmin):
    actions = ['download_csv_file']
    list_display = ('title', 'body', 'date_originally_posted')

    # whatever actions we use we have to define
    def download_csv_file(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from io import StringIO
        import time

        # for adding time to the csv file name
        time_stamp = time.strftime("%Y%m%d%H%M")

        # writing the string as a file
        file = StringIO()
        # writing the CSV file
        writer = csv.writer(file, delimiter = '|')
        # writing the headers
        writer.writerow(["Title", "Body", "Date_Originally_Posted"])

        # adding/writing whatever they add to the queryset
        # to the csv file
        for selected_set in queryset:
            writer.writerow([selected_set.title,
                            selected_set.body,
                            selected_set.date_originally_posted])
        # setting the seek at the begginning of the file
        file.seek(0)
        response = HttpResponse(file, content_type='text/csv')

        # the file name will be 'workIdeas' with the current time for organization reasons
        response['Content-Disposition'] = f'''attachment; filename=WorkIdeas_{time_stamp}.csv'''
        return response

    # displaying on admin page
    download_csv_file.short_description = "Download .csv file for what's selected."

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


class ThoughtsModel(models.Model):
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

    # automatically redirecting the user to the detail view after post creation
    def get_absolute_url(self):
        return reverse('thoughts-post-detail', kwargs={'pk': self.pk})



class ThoughtsAdmin(admin.ModelAdmin):
    actions = ['download_csv_file']
    list_display = ('title', 'body', 'date_originally_posted')

    def download_csv_file(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from io import StringIO
        import time

        time_stamp = time.strftime("%Y%m%d%H%M")
        file = StringIO()
        writer = csv.writer(file, delimiter="|")
        # detailing headers
        writer.writerow(["Title", "Body", "Date_Originally_Posted"])

        for selected_set in queryset:
            writer.writerow([selected_set.title,
                             selected_set.body,
                             selected_set.date_originally_posted])
        # setting the cursor at the beginning of the document
        # for the writing to be on the correct line
        file.seek(0)
        response = HttpResponse(file, content_type='text/csv')

        response['Content-Disposition'] = f'''attachment; filename=Thoughts_{time_stamp}.csv'''
        return response

    # displayed on the admin page
    download_csv_file.short_description = "Download .csv file for what's selected."

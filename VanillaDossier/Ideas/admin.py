from django.contrib import admin
from .models import IdeasModel


# for writing the selected model objects 
import csv
from django.http import HttpResponse
from io import StringIO
import time


# how the data is shown on the backend,
# also affects how the csv is dispayed
class IdeasAdmin(admin.ModelAdmin):
    actions = ['download_csv_file']
    list_display = ['title', 'body_excerpt', 'date_originally_posted']

    def body_excerpt(self, obj):
        return obj.get_body_excerpt(25)
        # return self.body[:num_of_characters]

    # whatever actions we use we have to define
    def download_csv_file(self, request, queryset):
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

        # the file name will be 'ideas' with the current time for organization reasons
        response['Content-Disposition'] = f'''attachment; filename=ideas_{time_stamp}.csv'''
        return response

    # displaying on admin page
    download_csv_file.short_description = "Download .csv file for what's selected."




admin.site.register(IdeasModel, IdeasAdmin)
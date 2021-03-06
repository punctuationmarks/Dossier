from django.contrib import admin

from .models import DossiersModel



class DossiersAdmin(admin.ModelAdmin):
    actions = ['download_csv_file']
    list_display = ('name', 'hobbies', 'work', 'appearance',
                    'notable_memories', 'discussions', 'date_originally_posted')

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
        writer = csv.writer(file, delimiter="|")

        # writing the headers
        writer.writerow['name', 'hobbies', 'work', 'appearance',
                        'notable_memories', 'discussions', 'date_originally_posted']

        # allowing the user to select what they want written in their
        # Django default of "selected_set"
        # csv file, looping over that and writing each row
        for selected_set in queryset:
            writer.writerow([selected_set.name,
                             selected_set.hobbies,
                             selected_set.work,
                             selected_set.appearance,
                             selected_set.notable_memories,
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




admin.site.register(DossiersModel, DossiersAdmin)

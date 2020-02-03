from django.contrib import admin

from .models import ThoughtsModel



class ThoughtsAdmin(admin.ModelAdmin):
    actions = ['download_csv_file']
    list_display = ['title', 'body_excerpt', 'date_originally_posted']

    def body_excerpt(self, obj):
        return obj.get_body_excerpt(25)
        # return self.body[:num_of_characters]



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




admin.site.register(ThoughtsModel, ThoughtsAdmin)

from django.db import models  # needed to user ORM
from django.utils import timezone  # for time data for post
from django.contrib.auth.models import User  # tieing the user to the post
from django.urls import reverse
from django.contrib import admin  # for admin view
# import datetime

class DossiersModel(models.Model):
    name = models.CharField(max_length=100)
    hobbies = models.CharField(max_length=300, blank=True)
    work = models.CharField(max_length=300, blank=True)
    appearance = models.CharField(max_length=100, blank=True)
    # field for specificities, like roommates' or cat's names
    notable_memories = models.CharField(max_length=100, blank=True)
    discussions = models.TextField(blank=True)
    # sets the datetime only to when the post is originally created,
    # you can never update the date posted argument
    date_originally_posted = models.DateTimeField(auto_now_add=True)

    # this will update the time, every time a post is updated
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_discussions_excerpt(self, num_of_characters):
        return self.discussions[:num_of_characters]

    def __str__(self):
        return f"""{self.name}, {self.date_originally_posted}"""

    # direct url for routing, based on primary key
    def get_absolute_url(self):
        return reverse('dossiers-detail', kwargs={'pk': self.pk})
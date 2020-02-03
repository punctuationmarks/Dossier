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



    def get_body_excerpt(self, num_of_characters):
        return self.body[:num_of_characters]


    def __str__(self):
        return f"{self.title}, {self.pk}"

    # automatically redirecting the user to the detail view after post creation
    def get_absolute_url(self):
        return reverse('thoughts-post-detail', kwargs={'pk': self.pk})
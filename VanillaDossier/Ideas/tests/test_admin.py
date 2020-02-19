
# importing Idea's model(s)
from .. import admin
from .. import models
from django.test import TestCase

# needed for making an instance of the Admin model
from django.contrib.admin.sites import AdminSite
# need for testing actions and what's visible with model
from django.contrib.auth.models import User


# imports needed for time
import time
# test imports
import pytest 
from mixer.backend.django import mixer
# pytest by default prevents database writing
# without this, it'll crash at the mixer call
# since mixer calls .save() after being called
pytestmark = pytest.mark.django_db




class TestIdeasAdmin(TestCase):
    # this is build for the download_csv_file() action
    # maybe make it so it doesn't run every time a test is run in admin?
    @classmethod
    def setUpTestData(cls):
        test_user_1 = User.objects.create_user(
            username="testuser1", password="testuser1")

        test_user_2 = User.objects.create_user(
            username="testuser2", password="testuser2")

        test_super_user = User.objects.create_superuser(username="super1",
                                                        email="email@email.com",
                                                        password="super1")

        test_user_1.save()
        test_user_2.save()
        test_super_user.save()

        ideas_randomly_generated = 32
        for i in range(1, ideas_randomly_generated):
            if i % 2 == 0:
                model_instance = mixer.blend(
                    'Ideas.IdeasModel', author=test_user_1)
            else:
                model_instance = mixer.blend(
                    'Ideas.IdeasModel', author=test_user_2)

    # testing the admin page has an excerpt of the body INSTEAD of the entire 
    # file
    def test_body_excerpt(self):
        # initializing an instance of AdminSite
        site = AdminSite()
        # having the admin site with the Ideas model
        ideas_admin = admin.IdeasAdmin(models.IdeasModel, site)
        obj = mixer.blend('Ideas.IdeasModel', title="Title 1", body="Hello world!")
        
        # calling the custom function, from the admin
        result = ideas_admin.body_excerpt(obj)
        
        # calling the custom function, from the model
        expected = obj.get_body_excerpt(25)
        
        assert result == expected, ('Should return the desired shortened string from the .excerpt() function')
        
    def test_download_csv_file_action_visibile(self):
        login = self.client.login(username="testuser1", password="testuser1")
        site = AdminSite()  
        # request = self.client.get(site, {'actions'})
        
        request = self.client.get(site)
        # print(request)
        
        
    # this is going to be more advanced than a basic crud, 
    # since we're dealing with csv writing, HttpResponses
    # and time, and a ['Content-Disposition']
    def test_download_csv_files(self):
        site = AdminSite()
        # having the admin site with the Ideas model
        ideas_admin = admin.IdeasAdmin(models.IdeasModel, site)
        obj_1 = mixer.blend('Ideas.IdeasModel', title="Title 1", body="Hello world! 1")
        obj_2 = mixer.blend('Ideas.IdeasModel', title="Title 2", body="Hello world! 2")
        
        time_now = time.strftime("%Y%m%d%H%M")
        # print("time_now", time_now)    
    
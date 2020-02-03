
# importing Idea's model(s)
from .. import admin
from .. import models

# needed for making an instance of the Admin model
from django.contrib.admin.sites import AdminSite



# imports needed for time
import time


# test imports
import pytest 
from mixer.backend.django import mixer
# pytest by default prevents database writing
# without this, it'll crash at the mixer call
# since mixer calls .save() after being called
pytestmark = pytest.mark.django_db




class TestThoughtsAdmin:
    # testing the admin page has an excerpt of the body INSTEAD of the entire 
    # file
    def test_body_excerpt(self):
        # initializing an instance of AdminSite
        site = AdminSite()
        # having the admin site with the Thoughts model
        thoughts_admin = admin.ThoughtsAdmin(models.ThoughtsModel, site)
        obj = mixer.blend('Thoughts.ThoughtsModel', title="Title 1", body="Hello world!")
        
        # calling the custom function, from the admin
        result = thoughts_admin.body_excerpt(obj)
        
        # calling the custom function, from the model
        expected = obj.get_body_excerpt(25)
        
        assert result == expected, ('Should return the desired shortened string from the .excerpt() function')
        
    # this is going to be more advanced than a basic crud, 
    # since we're dealing with csv writing, HttpResponses
    # and time, and a ['Content-Disposition']
    def test_download_csv_files(self):
        site = AdminSite()
        # having the admin site with the Thoughts model
        thoughts_admin = admin.ThoughtsAdmin(models.ThoughtsModel, site)
        obj_1 = mixer.blend('Thoughts.ThoughtsModel', title="Title 1", body="Hello world! 1")
        obj_2 = mixer.blend('Thoughts.ThoughtsModel', title="Title 2", body="Hello world! 2")
        
        # time_now = time.strftime("%Y%m%d%H%M")
        
        
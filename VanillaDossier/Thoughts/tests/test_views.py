# importing User to have new instances of users
from django.contrib.auth.models import User
from django.urls import reverse

import uuid
from Thoughts.models import ThoughtsModel

# testing imports
from django.test import TestCase
import pytest
from mixer.backend.django import mixer
# pytest by default prevents database writing
# without this boilerplate, it'll crash at the mixer call
# since mixer runs .save() after being called
pytestmark = pytest.mark.django_db


class ThoughtsViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user_1 = User.objects.create_user(
            username="test1", password="test1")
        test_user_2 = User.objects.create_user(
            username="test2", password="test2")
        test_super_user = User.objects.create_superuser(
            username="super1", password="super1", email="super1")

        test_user_1.save()
        test_user_2.save()
        test_super_user.save()

        # randomly generated posts
        x = 32
        for i in range(1, x):
            if i % 2 == 0:
                model_instance = mixer.blend(
                    'Thoughts.ThoughtsModel', author=test_user_1)
            else:
                model_instance = mixer.blend(
                    'Thoughts.ThoughtsModel', author=test_user_2)

        # specific titles and bodies to be searched
        y = 5
        for i in range(1, y):
            title = f"Great scott, ya thot! {i}"
            body = f"{i} starting at 1 to keep the indexes in line"

            if i % 2:
                author = test_user_1
            else:
                author = test_user_2

            ThoughtsModel.objects.create(
                title=title,
                body=body,
                author=author
            )
            
        # generating posts specificically for super user
        z = 5
        for i in range(z):
            title = f"Used for pagination of single page {i}!"
            body = f"{i}Lorem ipsum dolor sit amet consectetur adipisicing elit. Placeat, voluptatem quae. Reprehenderit, aspernatur. Qui, incidunt adipisci quisquam accusantium earum numquam."
            author = test_super_user

            ThoughtsModel.objects.create(
                title=title,
                body=body,
                author=author
            )
    
    def test_the_path_url_is_same_as_reverse_function(self):
        login = self.client.login(username="test1", password="test1")
        url = self.client.get('/thoughts/')
        response = self.client.get(reverse('thoughts'))
        # this is comparing the url paths
        assert url.request['PATH_INFO'] == response.request['PATH_INFO']
        
        # this is interesting, it fails somewhere I can't tell, visually it looks the same
        # is the same type of a class 'django.test.utils.ContextList'
        # and even py.test says where it fails, the code looks identical
        assert url != response
        assert url.context != response.context
        # but this is true: (where the actual non equivilance is stated in py.test)
        assert url.context["DEFAULT_MESSAGE_LEVELS"] == response.context["DEFAULT_MESSAGE_LEVELS"]    
    
    def test_redirect_when_user_not_logged_in(self):
        response = self.client.get(reverse('thoughts'))
        assert  response.status_code == 302
        assert response.url == "/admin/?next=/thoughts/"
    
    def test_showing_correct_template_when_user_logged_in(self):
        login = self.client.login(username="test1", password="test1")
        self.assertTrue(login)
        response = self.client.get(reverse('thoughts'))
            
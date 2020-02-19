from django.contrib.auth.models import User
from django.urls import reverse

import uuid
from Thoughts.models import ThoughtsModel

from django.test import TestCase
import pytest
from mixer.backend.django import mixer
# initializing pytest with django
pytestmark = pytest.mark.django_db


class ThoughtsViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user_1 = User.objects.create_user(
            username="testuser1", password="testuser1")
        test_user_2 = User.objects.create_user(
            username="testuser2", password="testuser2")
        test_super_user = User.objects.create_superuser(
            username="super1", password="super1", email="super1@email.com")

        test_user_1.save()
        test_user_2.save()
        test_super_user.save()

        # randomly generated posts
        num_of_blender_instances = 32
        for i in range(1, num_of_blender_instances):
            if i % 2 == 0:
                model_instance = mixer.blend(
                    'Thoughts.ThoughtsModel', author=test_user_1)
            else:
                model_instance = mixer.blend(
                    'Thoughts.ThoughtsModel', author=test_user_2)

        # specific titles and bodies to be searched
        num_of_searchable_instances = 5
        for i in range(1, num_of_searchable_instances):
            title = f"Great scott, thot! {i}"
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
        num_of_super_user_and_pagination_instances = 5
        for i in range(num_of_super_user_and_pagination_instances):
            title = f"Used for pagination of single page {i}!"
            body = f"{i}Lorem ipsum dolor sit amet consectetur adipisicing elit. Placeat, voluptatem quae. Reprehenderit, aspernatur. Qui, incidunt adipisci quisquam accusantium earum numquam."
            author = test_super_user

            ThoughtsModel.objects.create(
                title=title,
                body=body,
                author=author
            )


    def test_redirect_when_user_not_logged_in(self):
        response = self.client.get(reverse('thoughts'))
        
        assert response.status_code == 302
        assert response.url == "/admin/?next=/thoughts/"

    def test_the_path_url_is_same_as_reverse_function(self):
        login = self.client.login(username="testuser1", password="testuser1")
        url = self.client.get('/thoughts/')
        response = self.client.get(reverse('thoughts'))
        
        assert url != response
        assert url.context != response.context
        assert url.context["DEFAULT_MESSAGE_LEVELS"] == response.context["DEFAULT_MESSAGE_LEVELS"]
        assert url.request['PATH_INFO'] == response.request['PATH_INFO']
        
    def testing_the_user_has_been_logged_in(self):
        login = self.client.login(username="testuser1", password="testuser1")
        response = self.client.get(reverse('thoughts'))
        assert response.status_code == 200
        assert login == True
        
    def test_showing_correct_template_when_user_logged_in(self):
        login = self.client.login(username="testuser1", password="testuser1")    
        response = self.client.get(reverse('thoughts'))
        
        
        assert login == True
        assert response.status_code == 200
        
        self.assertTemplateUsed(response, "Thoughts/thoughtsmodel.html")

    def test_only_what_user_1_posts_can_be_seen_by_user_1(self):
        login = self.client.login(username="testuser1", password="testuser1")    
        response = self.client.get(reverse('thoughts'))
        thiry_one_thoughts = ThoughtsModel.objects.all()[:31]
        
        assert login == True
        assert str(response.context['user']) == "testuser1"
        assert response.status_code == 200
        assert 'posts' in response.context
        assert len(response.context['posts']) == 5
        
        for post in response.context['posts']:
            # print(post.author)
            assert response.context['user'] == post.author





    # how to do this?
    def test_users_posts_are_alphabetical(self):
        login = self.client.login(username="testuser1", password="testuser1")
        response = self.client.get(reverse('thoughts'))
        
        assert str(response.context['user']) == 'testuser1'
        assert response.status_code == 200
        
        assert 'posts' in response.context
        
        # this is 5 due to pagination declared in views.py
        # assert len(response.context['posts']) == 5
        
        # self.assertEqual(str(response.context['user']), 'testuser1')
        
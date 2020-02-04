from django.test import TestCase

# importing User to have new instances of users
from django.contrib.auth.models import User
from django.urls import reverse

# to make sure a 404 page comes up
import uuid

from Ideas.models import IdeasModel

# for generating psuedo data
import pytest
from mixer.backend.django import mixer
# pytest by default prevents database writing
# without this, it'll crash at the mixer call
# since mixer calls .save() after being called
pytestmark = pytest.mark.django_db


class IdeasViewslTest(TestCase):

    # this will be set up and run once at beginning of TestModel call
    # creating some users to allow the creation of some ideas to test
    # some basics
    @classmethod
    def setUpTestData(cls):
        test_user_1 = User.objects.create_user(
            username="testuser1", password="password1")

        test_user_2 = User.objects.create_user(
            username="testuser2", password="password2")

        test_super_user = User.objects.create_superuser(username="super1",
                                                        email="email@email.com",
                                                        password="super1")

        test_user_1.save()
        test_user_2.save()

        test_super_user.save()
        
        
        ideas_randomly_generated = 32
        for i in range(1, ideas_randomly_generated):
            if i % 2 ==0:
                model_instance = mixer.blend('Ideas.IdeasModel', author=test_user_1)            
            else:
                model_instance = mixer.blend('Ideas.IdeasModel', author=test_user_2)


        # generating ideas to be searched
        number_of_idea_entries = 5
        for i in range(1, number_of_idea_entries):
            idea_title = f"Great idea {i}!"
            idea_body = f"{i} starting at 1, to keep the indexes on the same interval as what is printed"

            if i % 2:
                idea_author = test_user_1
            else:
                idea_author = test_user_2

            IdeasModel.objects.create(
                title=idea_title,
                body=idea_body,
                author=idea_author
            )
        
        
        

        # creating ideas for super user

        # creating 31 instances of Ideas model
        number_of_idea_entries = 11
        for i in range(number_of_idea_entries):
            idea_super_title = f"Great idea {i}!"
            idea_super_body = f"Super cool stuff in here {i}"
            idea_super_author = test_super_user

            IdeasModel.objects.create(
                title=idea_super_title,
                body=idea_super_body,
                author=idea_super_author
            )
        # making sure the idea instance/object was created
        # print(IdeasModel.objects.first())

    '''
    My thoughts on this, is to make an actual user logged in site, so each user will 
    be siloed into their own "database" of ideas, thoughts, dossiers; but will have the possibility 
    of having multiple users to access the site. Could build it in such a way to deactivate
    this as well, so it'll be more of a single, private app (like how I want to use it, which 
    will be more secure) and then a public facing app for all the masses 
    
    - but the issue with this is that the "superuser" using this will have privilages
    '''
    # redirect URL is not correct, and not loading, test failing
    # no clue why, so this needs to be addressed ASAP

    def test_redirect_when_user_not_logged_in(self):
        response = self.client.get(reverse('ideas'))
        self.assertEqual(response.status_code, 302)

        # asserting the redirect is correct
        # print(response) # if you change the redirect url, check it here like this
        # print(response.url)
        assert response.url == "/admin/?next=/ideas/"

    # making sure the correct template is used

    def test_showing_correct_template_when_user_logged_in(self):
        # login returns a boolean by default
        login = self.client.login(username="testuser1", password="password1")
        # print(type(login))
        response = self.client.get(reverse('ideas'))

        # making sure it's the correct user, using the app
        self.assertEqual(str(response.context['user']), 'testuser1')
        # making sure the return is a 200 success code before checking the template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Ideas/ideasmodel.html")

    def test_only_what_user_1_posts_can_be_seen_by_user_1(self):
        login = self.client.login(username="testuser1", password="password1")
        response = self.client.get(reverse('ideas'))
        thirty_one_ideas = IdeasModel.objects.all()[:31]

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        # print(str(response.context))

        # making sure there are posts available
        self.assertTrue('posts' in response.context)

        # only ten here because it's paginating at 10 posts per page
        # the testuser1 actually has 15 posts
        # print(len(response.context['posts']))
        self.assertEqual(len(response.context['posts']), 10)

        # checking that all of the posts belong to the correct user
        for post in response.context['posts']:
            self.assertEqual(response.context['user'], post.author)

    def test_only_what_user_2_posts_can_be_seen_by_user_2(self):
        login = self.client.login(username="testuser2", password="password2")
        response = self.client.get(reverse('ideas'))
        thirty_one_ideas = IdeasModel.objects.all()[:31]

        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)

        # making sure there are posts available
        self.assertTrue('posts' in response.context)
        # only ten here because it's paginating at 10 posts per page
        # testuser2 actually has 16 posts
        # print(len(response.context['posts']))
        self.assertEqual(len(response.context['posts']), 10)

        # checking that all of the posts belong to the correct user
        for post in response.context['posts']:
            self.assertEqual(response.context['user'], post.author)

    # testing that super user can see everything (which means this is app is not
    # secure in a sense that I like. I don't like the idea of having someone being able
    # to read all of my dossier entries, so either keep the app siloed and open source,
    # or have it encrypted/anonymized for each user)

    def test_only_what_super_user_posts_can_be_seen_by_super_user(self):
        login = self.client.login(username="super1", password="super1")
        # print(login)
        response = self.client.get(reverse('ideas'))
        # print(response)
        super_user_ideas = IdeasModel.objects.all()[:11]
        # print(super_user_ideas)
        self.assertEqual(str(response.context['user']), 'super1')
        self.assertEqual(response.status_code, 200)

        # making sure there are posts available
        self.assertTrue('posts' in response.context)

        # only ten here because it's paginating at 10 posts per page
        self.assertEqual(len(response.context['posts']), 10)

        # checking that all of the posts belong to the correct user
        for post in response.context['posts']:
            # print(post.author)
            self.assertEqual(response.context['user'], post.author)

    # need to test that the posts are alphabetical and not by date
    # should I add feature to change the ordering?

    def test_all_ideas_are_ordered_by_title(self):
        login = self.client.login(username="testuser2", password="password2")
        response = self.client.get(reverse('ideas'))
        thirty_one_ideas = IdeasModel.objects.all()[:31]

        # is this necessary?
        for idea in thirty_one_ideas:
            idea.save()
            # print(str(idea))

        self.assertEqual(str(response.context['user']), 'testuser2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']), 10)

        # for idea in response.context['posts']:

    def test_search_page_feature_works_on_idea_title(self):
        login = self.client.login(username="testuser1", password="password1")
        response = self.client.get(reverse('ideas'), {'search': 'Great idea'})
        
        # print(len(response.context['posts']))
        # for post in response.context['posts']:
        #     print(post.body)
        #     print(post.author)
        
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertContains(response, 'Great idea')
        # "Something", "Should return the first few chracters of the body"


    def test_search_page_feature_works_on_idea_body(self):
        login = self.client.login(username="testuser1", password="password1")
        response = self.client.get(reverse('ideas'), {'search': 'indexes'})
        
        # print(len(response.context['posts']))
        # for post in response.context['posts']:
        #     print(post.body)
        #     print(post.author)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertContains(response, 'indexes')


    def test_search_page_feature_returns_0_posts_when_not_in_model_db(self):
        login = self.client.login(username="testuser1", password="password1")
        response = self.client.get(reverse('ideas'), {'search': 'not posted in this model'})
        
        # print(len(response.context['posts']))
        # for post in response.context['posts']:
        #     print(post.body)
        #     print(post.author)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']), 0)
        
        # self.assertContains(response, 'indexes')



    def test_alphabetical_ideas_posts(self):
        test_user_x = User.objects.create_user(
            username="testuserx", password="passwordx")

        test_user_x.save()
        
        login = self.client.login(username="testuserx", password="passwordx")
        
        # print(login)
        ideas_generated = 10
        for index in range(ideas_generated):
            model_instance = mixer.blend(
                'Ideas.IdeasModel', author=test_user_x)
            # print(model_instance)
        response = self.client.get(reverse('ideas'))
        
        # assert that the response.posts is in alphebtical order, 
        # do I need to have an "alphabet"  to loop over or is this built into Django/Python? geeeezzzz
        
        # print(response)
        # assert result == "Something", "Should return the first few chracters of the body"

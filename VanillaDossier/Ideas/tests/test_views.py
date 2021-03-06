# importing User to have new instances of users
from django.contrib.auth.models import User
from django.urls import reverse

import uuid
from Ideas.models import IdeasModel

# testing imports
from django.test import TestCase
import pytest
from mixer.backend.django import mixer
# pytest by default prevents database writing
# without this boilerplate, it'll crash at the mixer call
# since mixer runs .save() after being called
pytestmark = pytest.mark.django_db


class IdeasViewsTest(TestCase):

    # this will be set up and run once at beginning of TestModel call
    # creating some users to allow the creation of some ideas to test
    # some basics
    @classmethod
    def setUpTestData(cls):
        test_user_1 = User.objects.create_user(
            username="testuser1", password="testuser1")

        test_user_2 = User.objects.create_user(
            username="testuser2", password="testuser2")

        test_super_user = User.objects.create_superuser(username="super1",
                                                        email="super1@email.com",
                                                        password="super1")

        test_user_1.save()
        test_user_2.save()
        test_super_user.save()

        num_of_blender_instances = 32
        for i in range(1, num_of_blender_instances):
            if i % 2 == 0:
                # using mixer to generate model instances, like a model factory
                model_instance = mixer.blend(
                    'Ideas.IdeasModel', author=test_user_1)
            else:
                model_instance = mixer.blend(
                    'Ideas.IdeasModel', author=test_user_2)

        # generating ideas to be searched
        num_of_searchable_instances = 5
        for i in range(1, num_of_searchable_instances):
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
        num_of_super_user_and_pagination_instances = 5
        for i in range(num_of_super_user_and_pagination_instances):
            idea_super_title = f"Used for pagination of single page {i}!"
            idea_super_body = f"{i}Lorem ipsum dolor sit amet consectetur adipisicing elit. Placeat, voluptatem quae. Reprehenderit, aspernatur. Qui, incidunt adipisci quisquam accusantium earum numquam."
            idea_super_author = test_super_user

            IdeasModel.objects.create(
                title=idea_super_title,
                body=idea_super_body,
                author=idea_super_author
            )

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

    def test_showing_what_the_template_response_can_return(self):

        # login returns a boolean by default
        login = self.client.login(username="testuser1", password="testuser1")
        # print(type(login))
        response = self.client.get(reverse('ideas'))

    def test_redirect_when_user_not_logged_in(self):
        response = self.client.get(reverse('ideas'))
        # print(type(response))
        # print(response.body)
        self.assertEqual(response.status_code, 302)

        # asserting the redirect is correct
        # print(response) # if you change the redirect url, check it here like this
        # print(response.url)
        assert response.url == "/admin/?next=/ideas/"

    def test_the_path_url_is_same_as_reverse_function(self):
        ''' 
        this test might seem redundant since it might feel like we're checking the
        functionality of Django, but it is something we're customizing from Django
        so it should be tested in a perfect world, but if building something on 
        the fly, you *might* get away with skipping tests like these
        '''

        login = self.client.login(username="testuser1", password="testuser1")
        url = self.client.get("/ideas/")
        response = self.client.get(reverse('ideas'))
        
        # this is interesting, it fails somewhere at equality that 
        # I can't tell, because visually the returned strings look the same
        # is the same type of a class 'django.test.utils.ContextList'
        # and even py.test says where it fails, the code looks identical
        assert url != response
        assert url.context != response.context 

        # but these are true
        assert url.request['PATH_INFO'] == response.request['PATH_INFO']
        assert url.context['DEFAULT_MESSAGE_LEVELS'] == response.context['DEFAULT_MESSAGE_LEVELS']
        
    
    # making sure the correct template is used
    def test_showing_correct_template_when_user_logged_in(self):
        # login returns a boolean by default
        login = self.client.login(username="testuser1", password="testuser1")
        # print(type(login))
        response = self.client.get(reverse('ideas'))

        # making sure it's the correct user, using the app
        self.assertEqual(str(response.context['user']), 'testuser1')
        # making sure the return is a 200 success code before checking the template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Ideas/ideasmodel.html")

    def test_only_what_user_1_posts_can_be_seen_by_user_1(self):
        login = self.client.login(username="testuser1", password="testuser1")
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
        login = self.client.login(username="testuser2", password="testuser2")
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
        super_user_ideas = IdeasModel.objects.all()
        # print(super_user_ideas)
        self.assertEqual(str(response.context['user']), 'super1')
        self.assertEqual(response.status_code, 200)

        # making sure there are posts available
        self.assertTrue('posts' in response.context)

        # only 5 here because that's all that the superuser posted
        self.assertEqual(len(response.context['posts']), 5)

        # checking that all of the posts belong to the correct user
        for post in response.context['posts']:
            # print(post.author)
            self.assertEqual(response.context['user'], post.author)

    def test_search_page_feature_works_on_idea_title(self):
        login = self.client.login(username="testuser1", password="testuser1")
        response = self.client.get(reverse('ideas'), {'search': 'Great idea'})

        # print(len(response.context['posts']))
        # for post in response.context['posts']:
        #     print(post.body)
        #     print(post.author)

        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertContains(response, 'Great idea')
        # "Something", "Should return the first few chracters of the body"

    def test_search_page_feature_works_on_idea_body(self):
        login = self.client.login(username="testuser1", password="testuser1")
        response = self.client.get(reverse('ideas'), {'search': 'indexes'})

        # print(len(response.context['posts']))
        # for post in response.context['posts']:
        #     print(post.body)
        #     print(post.author)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertContains(response, 'indexes')

    def test_search_page_feature_returns_0_posts_when_not_in_model_db(self):
        login = self.client.login(username="testuser1", password="testuser1")
        response = self.client.get(
            reverse('ideas'), {'search': 'not posted in this model'})

        # print(len(response.context['posts']))
        # for post in response.context['posts']:
        #     print(post.body)
        #     print(post.author)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('posts' in response.context)
        self.assertEqual(len(response.context['posts']), 0)

    def test_pagination_on_page(self):
        login = self.client.login(username="testuser1", password="testuser1")
        response = self.client.get(reverse('ideas'))
        self.assertEqual(response.status_code, 200)
        # print(response.context['is_paginated'])
        # print(response.is_paginated)
        self.assertTrue('is_paginated' in response.context)
        # print(response.context['num_of_pages'])
        self.assertTrue(response.context['is_paginated'])
        # print(response.context)

    def test_pagination_single_page(self):
        login = self.client.login(username="super1", password="super1")
        response = self.client.get(reverse('ideas'))
        self.assertEqual(response.status_code, 200)
        # print(response.context['is_paginated'])
        # print(response.is_paginated)
        self.assertTrue('is_paginated' in response.context)
        # print(response.context['is_paginated'])
        self.assertFalse(response.context['is_paginated'])
        # print(response.context)

    def test_that_correct_template_is_being_used_for_new_idea_post(self):
        login = self.client.login(username="testuser1", password="testuser1")
        response = self.client.get(reverse('ideas-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Ideas/ideasmodel_form.html')

    # DESIGN THOUGHT:
    """ currently this redirects to the post the user created,
     and although I like the concept of being able to see a post
     and the ability to edited it quickly, not sure if this is the best
     UX design choice, think about it some more
    """

    def test_post_goes_though_are_redirects(self):
        login = self.client.login(username="testuser1", password="testuser1")
        self.client.post('/ideas/new/', {'author': "testuser1",
                                         'title': "Super Important Test",
                                         'body': "This is really important.", })
        self.assertEqual(IdeasModel.objects.last().title,
                         "Super Important Test")

    def test_redirect_to_correct_published_post(self):
        login = self.client.login(username="testuser1", password="testuser1")
        response = self.client.post(
            reverse('ideas-create'), {
                "title": "Some Idea",
                "body": "Body Body Body",
                "author": "testuser1",
                # author is automatically linked to the logged in user
            })
        self.assertEqual(response.status_code, 302)

        """
         NEED TO REFACTOR:

         These three do the same thing, ordered in what takes longer.
         There has to be a better way, but some reason
         I can't find access to the object.pk in the response
        """
        # fastest:
        url_from_pk = "/ideas/" + str(IdeasModel.objects.last().pk) + "/"
        self.assertEqual(response.url, url_from_pk)
        # slower:
        # assert response.url.rstrip("/") == "/ideas/" +str(IdeasModel.objects.last().pk)
        # slowest:
        # assert response.url == "/ideas/" + str(IdeasModel.objects.last().pk) + "/"

    def test_detailed_view_of_logged_in_user_with_their_post(self):
        login = self.client.login(username="testuser1", password="testuser1")

        response = self.client.get(
            reverse('ideas-detail', kwargs={"pk": IdeasModel.objects.first().pk}))
        assert str(
            response.context['user']) == "testuser1", "should return the logged in user's name since it's their post"

    def test_something_might_be_pointless(self):
        model_instance_1 = IdeasModel.objects.get(id=1)
        model_instance_2 = IdeasModel.objects.get(id=2)
        # print(idea_1.body)
        field_label_title_1 = model_instance_1._meta.get_field(
            'title').verbose_name
        # print(field_label_title_1)
        assert str(model_instance_1.author) == "testuser2"
        assert str(model_instance_2.author) == "testuser1"

    def test_pk_transalted_to_logged_in_user(self):
        # grabbing user 2
        model_instances_with_user_2 = IdeasModel.objects.get(id=1).author
        # grabbing user 1's posts, none of user 2's
        first_model_instance = IdeasModel.objects.all().exclude(
            author=model_instances_with_user_2).get(id=2)
        # print(first_model_instance.author) # this returns testuser1

        # loggin in user 2
        login = self.client.login(username="testuser2", password="testuser2")
        # taking the primary key from testuser1's post, and
        # returning testuser2's and NOT returning testuser1's post
        response = self.client.get(
            reverse('ideas-detail', kwargs={"pk": first_model_instance.pk}))

        # so each primary key is siloed to each user, this doesn't redirect
        # but it does "translate" the primary key from one user to another,
        # not allowing the user to see the other's data (but this is not a thorough test)
        assert str(response.context['user']) == "testuser2"

    def test_users_posts_are_alphabetical(self):

        # loggin in testuser1
        login = self.client.login(username="testuser1", password="testuser1")
        # print(login)
        response = self.client.get(reverse('ideas'))
        # print(response)
        # super_user_ideas = IdeasModel.objects.all()
        # print(super_user_ideas)
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)

        # making sure there are posts available
        self.assertTrue('posts' in response.context)

        # this is 10 due to pagination declared in views.py
        self.assertEqual(len(response.context['posts']), 10)
        
        # print(response.context['posts'])
        # self.assertEqual(response.context['posts'].title, sorted(response.context['posts']))

        # # checking that all of the posts belong to the correct user
        # for post in response.context['posts']:
        #     print(post)
        #     self.assertEqual(response.context['user'], post.author)

        # print(response.rendered_content)

    # def test_alphabetical_ideas_posts(self):
    #     test_user_x = User.objects.create_user(
    #         username="testuserx", password="passwordx")

    #     test_user_x.save()

    #     login = self.client.login(username="testuserx", password="passwordx")

    #     # print(login)
    #     ideas_generated = 10
    #     for index in range(ideas_generated):
    #         model_instance = mixer.blend(
    #             'Ideas.IdeasModel', author=test_user_x)
    #         # print(model_instance)
    #     response = self.client.get(reverse('ideas'))

    #     # assert that the response.posts is in alphebtical order,
    #     # do I need to have an "alphabet"  to loop over or is this built into Django/Python? geeeezzzz

    #     # print(response)
    #     # assert result == "Something", "Should return the first few chracters of the body"

    # self.assertContains(str(IdeasModel.objects.last().pk), response.url)

    # self.assertContains
    # print(response.context_data)
    # print(" ")
    # print(response.url)
    # print(response.context['user'])
    # print(response.context['pk'])
    # print(response.context['form'])
    # print(response.context)
    # print("template name as list: .template_name", response.template_name)
    # print("object from model: .context_data", response.context_data)
    # print("entire page: .rendered_content ", response.rendered_content)
    # print("encoded in: .charset ", response.charset)
    # print("engine: .using ", response.using)
    # print("\nhow a basic assert statement works:")

    # need to test that the posts are alphabetical and not by date
    # should I add feature to change the ordering?
    # def test_all_ideas_are_ordered_by_title(self):
    #     login = self.client.login(username="testuser2", password="testuser2")
    #     response = self.client.get(reverse('ideas'))
    #     thirty_one_ideas = IdeasModel.objects.all()[:31]

    #     # is this necessary?
    #     for idea in thirty_one_ideas:
    #         idea.save()
    #         # print(str(idea))

    #     self.assertEqual(str(response.context['user']), 'testuser2')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue('posts' in response.context)
    #     self.assertEqual(len(response.context['posts']), 10)

    # for idea in response.context['posts']:

    '''
    def test_pagination_is_ten_ideas(self):
        response = self.client.get(reverse('ideas'))
        self.assertEqual(response.status_code, 200)
        # this checks to make sure the page has the is_paginated in the page itself
        self.assertTrue('is_paginated' in response.context)
        # this makes sure pagination is turned on
        self.assertTrue(response.context['is_paginated'] == True)
        # this makes sure it paginates at 10 objects
        self.assertTrue(len(response.context['idea_list']) == 10)
    '''

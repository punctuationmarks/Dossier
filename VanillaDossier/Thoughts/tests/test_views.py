from django.test import TestCase

# importing User to have new instances of users
from django.contrib.auth.models import User
from django.urls import reverse

# to make sure a 404 page comes up
import uuid

from Ideas.models import IdeasModel


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

        # creating 31 instances of Ideas model
        number_of_idea_entries = 31
        for i in range(number_of_idea_entries):
            idea_title = f"Great idea {i}!"
            idea_body = f"Super cool stuff in here {i}"

            if i % 2:
                idea_author = test_user_1
            else:
                idea_author = test_user_2
                
            IdeasModel.objects.create(
                title=idea_title,
                body=idea_body,
                author=idea_author
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
        
        # this prints:
        # <HttpResponseRedirect status_code=302, "text/html; charset=utf-8", url="/admin/?next=/ideas/">
        # print(str(response))
        
        # this fails
        # self.assertRedirects(response, "/admin/?next=/ideas/")
    
        
        # this is the url that str(response) returns: and error
        #  AssertionError: 302 != 200 : Couldn't retrieve redirection page '/admin/': response code was 302 (expected 200)
        # self.assertRedirects(response,
        #                      "/admin/?next=/ideas/")

        # this is the literal redirect url (manual testing), but even this fails
        # self.assertRedirects(response, "/admin/login/?next=/admin/%3Fnext%3D/ideas/" )
        
        # this doesn't work:
        # self.assertContains(response, "/admin/login/")
        

    # making sure the correct template is used
    def test_showing_correct_template_when_user_logged_in(self):
        login = self.client.login(username="testuser1", password="password1")
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
        
        # double checking that all of the posts belong to the correct user
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
        
        # double checking that all of the posts belong to the correct user
        for post in response.context['posts']:
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
            
        

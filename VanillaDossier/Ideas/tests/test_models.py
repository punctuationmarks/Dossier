from django.test import TestCase

# importing User to have new instances of users 
from django.contrib.auth.models import User 
from django.urls import reverse 


# importing Idea's model(s)
from Ideas.models import IdeasModel


import pytest 
from mixer.backend.django import mixer
# pytest by default prevents database writing
# without this, it'll crash at the mixer call
# since mixer calls .save() after being called
pytestmark = pytest.mark.django_db


class IdeasModelTest(TestCase):
    
    # this will be set up and run once at beginning of TestModel call
    # creating some users to allow the creation of some ideas to test
    # some basics
    @classmethod
    def setUpTestData(cls):
        test_user_1 = User.objects.create_user(username="testuser1", password="password1")
        test_user_2_super = User.objects.create_superuser(username="super1",
                                                          email="email@email.com", 
                                                          password="super1")
        
        test_user_1.save()
        test_user_2_super.save()
        
        # creating 10 instances of Ideas model
        number_of_idea_entries = 10
        for i in range(number_of_idea_entries):
            idea_title = f"Great idea {i}!"
            idea_body = f"{i} Lorem ipsum dolor sit amet consectetur adipisicing elit. Corporis accusamus ab sunt dolorem, facere veritatis ducimus temporibus sapiente non voluptas, veniam iusto quas? Ea, enim tempore. Iste quibusdam repudiandae suscipit."

            if i % 2:
                idea_author = test_user_1
            else:
                idea_author = test_user_2_super
            
            IdeasModel.objects.create(
                title = idea_title,
                body = idea_body,
                author = idea_author
            )

    def test_something_might_be_pointless(self):
        model_instance_1 = IdeasModel.objects.get(id=1)
        model_instance_2 = IdeasModel.objects.get(id=2)
        # print(idea_1.body)
        field_label_title_1 = model_instance_1._meta.get_field('title').verbose_name
        
    
    def test_title_max_length(self):
        model_instance = IdeasModel.objects.get(id=1)
        title_max_length = model_instance._meta.get_field('title').max_length
        self.assertEqual(title_max_length, 100)
    
    # this is testing the __str__ override
    def test_overriding_str_function(self):
        model_instance = IdeasModel.objects.get(id=1)
        expected_return = f'{model_instance.title}, {model_instance.pk}'
        self.assertEqual(expected_return, str(model_instance))
    
        
    # testing the overridden get_absolute_url
    def test_get_absolute_url(self):
        model_instance = IdeasModel.objects.get(id=1)
        # this is the "absolute" url, not the reverse route name
        self.assertEqual(model_instance.get_absolute_url(), '/ideas/1/')
        
        
    # using mixer to make some psuedo data
    # this is kinda nice because you can user smaller, more flexible data and easier to read than lorem ipsum 
    def test_get_body_excerpt(self):
        
        model_instance = mixer.blend('Ideas.IdeasModel', title="Title 1", body="Something here")
        result = model_instance.get_body_excerpt(9)
        # print(result)
        assert result == "Something", "Should return the first few chracters of the body"
    
# for instance of user
from django.contrib.auth.models import User 
# for ease of urls, tested it works first
from django.urls import reverse 
# importing Thought's model(s)
from Thoughts.models import ThoughtsModel


# testing imports
from django.test import TestCase
import pytest 
from mixer.backend.django import mixer
# pytest by default prevents database writing
# without this boilerplate, it'll crash at the mixer call
# since mixer runs .save() after being called
pytestmark = pytest.mark.django_db


class ThoughtsModelTest(TestCase):
    
    # this will be set up and run once at beginning of TestModel call
    # creating some users to allow the creation of some thoughts to test
    # some basics
    @classmethod
    def setUpTestData(cls):
        test_user_1 = User.objects.create_user(username="testuser1", password="password1")
        test_user_2_super = User.objects.create_superuser(username="super1",
                                                          email="email@email.com", 
                                                          password="super1")
        
        test_user_1.save()
        test_user_2_super.save()
        
        # creating 10 instances of Thoughts model
        number_of_thought_entries = 10
        for i in range(1, number_of_thought_entries):
            thought_title = f"Great thought {i}!"
            thought_body = f"{i} Lorem ipsum dolor sit amet consectetur adipisicing elit. Corporis accusamus ab sunt dolorem, facere veritatis ducimus temporibus sapiente non voluptas, veniam iusto quas? Ea, enim tempore. Iste quibusdam repudiandae suscipit."

            if i % 2 ==0:
                thought_author = test_user_1
            else:
                thought_author = test_user_2_super
            
            ThoughtsModel.objects.create(
                title = thought_title,
                body = thought_body,
                author = thought_author
            )

    def test_something_might_be_pointless(self):
        model_instance_1 = ThoughtsModel.objects.get(id=1)
        model_instance_2 = ThoughtsModel.objects.get(id=2)
        # print(thought_1.body)
        field_label_title_1 = model_instance_1._meta.get_field('title').verbose_name
        
    
    def test_title_max_length(self):
        model_instance = ThoughtsModel.objects.get(id=1)
        title_max_length = model_instance._meta.get_field('title').max_length
        self.assertEqual(title_max_length, 100)
    
    # this is testing the __str__ override
    def test_overriding_str_function(self):
        model_instance = ThoughtsModel.objects.get(id=1)
        expected_return = f'{model_instance.title}, {model_instance.pk}'
        self.assertEqual(expected_return, str(model_instance))
    
        
    # testing the overridden get_absolute_url
    def test_get_absolute_url(self):
        model_instance = ThoughtsModel.objects.get(id=1)
        # this is the "absolute" url, not the reverse route name
        self.assertEqual(model_instance.get_absolute_url(), '/thoughts/1/')
        
        
    # using mixer to make some psuedo data
    # this is kinda nice because you can user smaller, more flexible data and easier to read than lorem ipsum 
    def test_get_body_excerpt(self):
        
        model_instance = mixer.blend('Thoughts.ThoughtsModel', title="Title 1", body="Something here")
        result = model_instance.get_body_excerpt(9)
        # print(result)
        assert result == "Something", "Should return the first few chracters of the body"
    
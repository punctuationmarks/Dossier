from django.test import TestCase

# importing User to have new instances of users 
from django.contrib.auth.models import User 
from django.urls import reverse 


import datetime

# importing Idea's model(s)
from Dossiers.models import DossiersModel


import pytest 
from mixer.backend.django import mixer
# pytest by default prevents database writing
# without this, it'll crash at the mixer call
# since mixer calls .save() after being called
pytestmark = pytest.mark.django_db


class TestDossiersModel(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        test_user_1 = User.objects.create_user(username="testUser", password="password")
        test_user_2_super = User.objects.create_superuser(username="superUser",
                                                          email="email@email.com", 
                                                          password="superUser")
        
        test_user_1.save()
        test_user_2_super.save()
        
        number_of_dossier_entries = 10
        for i in range(1, number_of_dossier_entries):
            if i % 2 == 0:
                dossier_object = mixer.blend('Dossiers.DossiersModel', 
                                             name=f"Billy Goat {i}",
                                             hobbies=f"Skiing {i}",
                                             work=f"Sign Spinner {i}",
                                             appearance=f"looks like the number {i}",
                                             notable_memories = f"{i} ate {i} like a snake", 
                                             discussions = f"We talked about the infinite {i}",
                                             author=test_user_1)
            else:
                # random data populated by mixer
                dossier_object = mixer.blend('Dossiers.DossiersModel', author=test_user_2_super)
            # print(dossier_object.name)
        # help(mixer.blend)

    # this is just testing that the model can have an instance
    # def test_model(self):
    #     model_instance = mixer.blend('Dossiers.DossiersModel')
    #     # assert that something is equivallent to, and what message to print to screen
    #     # (to keep track of tests)
    #     # the second message serves as a type of developer documentation
    #     # write this in prose, so it's easy to understand so you can debug it years later
    #     assert model_instance.pk == 1, "Should create a DossiersModel instance"

        
    # we want an except of the body, since we don't want a 500 character body text
    def test_get_excerpt(self):
        model_instance = mixer.blend('Dossiers.DossiersModel', discussions="Hello, Jon. You must fix the TV now.")
        # calling get_except function with the first few characters
        result = model_instance.get_discussions_excerpt(5)
        assert result == "Hello", "Should return the first few characters"


    def test_return_correct_fields_all_fields(self):
        model_instance = DossiersModel.objects.get(id=2)
        assert model_instance.name == "Billy Goat 2"
        assert model_instance.hobbies == "Skiing 2"
        assert model_instance.work == "Sign Spinner 2"
        assert model_instance.appearance == "looks like the number 2"
        assert model_instance.notable_memories == "2 ate 2 like a snake"
        assert model_instance.discussions == "We talked about the infinite 2"
        assert str(model_instance.author) == "testUser"





# testing alterations to default fields
    def test_name_max_length(self):
        model_instance = DossiersModel.objects.get(id=1)
        name_max_length = model_instance._meta.get_field('name').max_length
        self.assertEqual(name_max_length, 100)

    def test_hobbies_max_length(self):
        model_instance = DossiersModel.objects.get(id=1)
        hobbies_max_length = model_instance._meta.get_field('hobbies').max_length
        self.assertEqual(hobbies_max_length, 300)
    
    def test_work_max_length(self):
        model_instance = DossiersModel.objects.get(id=1)
        work_max_length = model_instance._meta.get_field('work').max_length
        self.assertEqual(work_max_length, 300)    
    
    def test_appearance_max_length(self):
        model_instance = DossiersModel.objects.get(id=1)
        appearance_max_length = model_instance._meta.get_field('appearance').max_length
        self.assertEqual(appearance_max_length, 100)

    def test_notable_memories_max_length(self):
        model_instance = DossiersModel.objects.get(id=1)
        notable_memories_max_length = model_instance._meta.get_field('notable_memories').max_length
        self.assertEqual(notable_memories_max_length, 100)

    def test_overriding_str_function(self):
        model_instance = DossiersModel.objects.get(id=1)
        expected_return = f'{model_instance.name}, {model_instance.date_originally_posted}'
        self.assertEqual(expected_return, str(model_instance))

    def test_get_absolute_url(self):
        model_instance_1 = DossiersModel.objects.get(id=1)
        model_instance_2 = DossiersModel.objects.get(id=2)

        self.assertEqual(model_instance_1.get_absolute_url(), '/dossiers/1/')
        self.assertEqual(model_instance_2.get_absolute_url(), '/dossiers/2/')

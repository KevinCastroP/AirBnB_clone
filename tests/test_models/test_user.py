#!/usr/bin/python3
'''Tests for User class'''
import models
import os
import os.path
import unittest
from models.user import User
from models.engine import file_storage
from models.engine.file_storage import FileStorage


class Test_User(unittest.TestCase):
    '''start tests'''

    def test_docstring(self):
        '''test if funcions, methods, classes
        and modules have docstring'''
        msj = "Módulo does not has docstring"
        self.assertIsNotNone(models.user.__doc__, msj)  # Modules
        msj = "Clase does not has docstring"
        self.assertIsNotNone(User.__doc__, msj)  # Classes

    def test_executable_file(self):
        '''test if file has permissions u+x to execute'''
        # Check for read access
        is_read_true = os.access('models/user.py', os.R_OK)
        self.assertTrue(is_read_true)
        # Check for write access
        is_write_true = os.access('models/user.py', os.W_OK)
        self.assertTrue(is_write_true)
        # Check for execution access
        is_exec_true = os.access('models/user.py', os.X_OK)
        self.assertTrue(is_exec_true)

    def test_is_an_instance(self):
        '''check if my_model is an instance of User'''
        my_model = User()
        self.assertIsInstance(my_model, User)

    def test_id(self):
        '''test if the id of two instances are different'''
        my_model = User()
        my_model1 = User()
        self.assertNotEqual(my_model.id, my_model1.id)

    def test_str(self):
        '''check if the output of str is in the specified format'''
        my_model4 = User()
        _dict = my_model4.__dict__
        string1 = "[User] ({}) {}".format(my_model4.id, _dict)
        string2 = str(my_model4)
        self.assertEqual(string1, string2)

    def test_save(self):
        '''check if the attribute updated_at (date) is updated for
        the same object with the current date'''
        my_model2 = User()
        first_updated = my_model2.updated_at
        my_model2.save()
        second_updated = my_model2.updated_at
        self.assertNotEqual(first_updated, second_updated)

    def test_to_dict(self):
        '''check if to_dict returns a dictionary, if add a class
        key with class name of the object and if updated_at and
        created_at are converted to string object in ISO format.'''
        my_model3 = User()
        my_dict_model3 = my_model3.to_dict()
        self.assertIsInstance(my_dict_model3, dict)
        for key, value in my_dict_model3.items():
            flag = 0
            if my_dict_model3['__class__'] == 'User':
                flag += 1
            self.assertTrue(flag == 1)
        for key, value in my_dict_model3.items():
            if key == 'created_at':
                self.assertIsInstance(value, str)
            if key == 'updated_at':
                self.assertIsInstance(value, str)

    def test_kwargs(self):
        '''check when a dictionary in sent as **kwargs argument'''
        my_model = User()
        my_model.name = "Holberton"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_model_kwargs = User(**my_model_json)
        self.assertNotEqual(my_model_kwargs, my_model)

    def test_des_and_serialization(self):
        '''check serialization and deserialization'''
        storage = FileStorage()
        all_objs = storage.all()
        self.assertIsInstance(all_objs, dict, "es diccionario")  # Test all
        my_model = User()
        my_model.name = "Paparoachchchch"
        my_model.my_number = 95
        my_model.save()
        with open("file.json", "r", encoding='utf-8') as f:
            self.assertTrue(my_model.name in f.read())  # Test save

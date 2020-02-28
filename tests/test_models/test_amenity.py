#!/usr/bin/python3
'''Tests for Amenity class'''
import models
import os
import os.path
import unittest
from models.amenity import Amenity
from models.engine import file_storage
from models.engine.file_storage import FileStorage


class TestAmenity(unittest.TestCase):
    '''start tests'''

    def setUp(self):
        '''Object created from a class'''
        self.my_object = Amenity()

    def test_docstring(self):
        '''test if funcions, methods, classes
        and modules have docstring'''
        msj = "Módulo does not has docstring"
        self.assertIsNotNone(models.amenity.__doc__, msj)  # Modules
        msj = "Clase does not has docstring"
        self.assertIsNotNone(Amenity.__doc__, msj)  # Classes

    def test_executable_file(self):
        '''test if file has permissions u+x to execute'''
        # Check for read access
        is_read_true = os.access('models/amenity.py', os.R_OK)
        self.assertTrue(is_read_true)
        # Check for write access
        is_write_true = os.access('models/amenity.py', os.W_OK)
        self.assertTrue(is_write_true)
        # Check for execution access
        is_exec_true = os.access('models/amenity.py', os.X_OK)
        self.assertTrue(is_exec_true)

    def test_is_an_instance(self):
        '''check if my_object is an instance of Amenity'''
        self.assertIsInstance(self.my_object, Amenity)

    def test_id(self):
        '''test if the id of two instances are different'''
        instance1 = Amenity()
        instance2 = Amenity()
        self.assertNotEqual(instance1.id, instance2.id)

    def test_str(self):
        '''check if the output of str is in the specified format'''
        _dict = self.my_object.__dict__
        string1 = "[Amenity] ({}) {}".format(self.my_object.id, _dict)
        string2 = str(self.my_object)
        self.assertEqual(string1, string2)

    def test_save(self):
        '''check if the attribute updated_at (date) is updated for
        the same object with the current date'''
        first_updated = self.my_object.updated_at
        self.my_object.save()
        second_updated = self.my_object.updated_at
        self.assertNotEqual(first_updated, second_updated)
        os.remove("file.json")

    def test_to_dict(self):
        '''check if to_dict returns a dictionary, if add a class
        key with class name of the object and if updated_at and
        created_at are converted to string object in ISO format.'''
        my_dict_model = self.my_object.to_dict()
        self.assertIsInstance(my_dict_model, dict)
        for key, value in my_dict_model.items():
            flag = 0
            if my_dict_model['__class__'] == 'Amenity':
                flag += 1
            self.assertTrue(flag == 1)
        for key, value in my_dict_model.items():
            if key == 'created_at':
                self.assertIsInstance(value, str)
            if key == 'updated_at':
                self.assertIsInstance(value, str)

    def test_kwargs(self):
        '''check when a dictionary in sent as **kwargs argument'''
        self.my_object.name = "Holberton"
        self.my_object.my_number = 89
        my_object_json = self.my_object.to_dict()
        my_object_kwargs = Amenity(**my_object_json)
        self.assertNotEqual(my_object_kwargs, self.my_object)

    def test_des_and_serialization(self):
        '''check serialization and deserialization'''
        storage = FileStorage()
        all_objs = storage.all()
        self.assertIsInstance(all_objs, dict, "es diccionario")  # Test all
        self.my_object.name = "Paparoachchchch"
        self.my_object.my_number = 95
        self.my_object.save()
        with open("file.json", "r", encoding='utf-8') as f:
            self.assertTrue(self.my_object.name in f.read())  # Test save

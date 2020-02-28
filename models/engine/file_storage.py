#!/usr/bin/python3
"""
Filestorage funtion all, new, save, reload
"""
import json
import os.path
from models.base_model import BaseModel
from models.user import User


class FileStorage():
    """ Init"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Returns dict """
        return type(self).__objects

    def new(self, obj):
        """ Sets new object in dictionary """
        if obj:
            self.__objects["{}.{}".format(
                obj.__class__.__name__, obj.id)] = obj

    def save(self):
        """ Serializes __objects = {}"""
        new_jhoson_file = {}
        with open(self.__file_path, mode="w") as jfile:
            for key, value in self.__objects.items():
                new_jhoson_file[key] = value.to_dict()
                """JSON encoder and decoder"""
            json.dump(new_jhoson_file, jfile)

    def reload(self):
        """ Deserializes __objects = {}"""
        if os.path.isfile(self.__file_path):
            with open(self.__file_path, mode="r") as jfile:
                for key, value in json.load(jfile).items():
                    new_obj = eval(value["__class__"])(**value)
                    self.__objects[key] = new_obj

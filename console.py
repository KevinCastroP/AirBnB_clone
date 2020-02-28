#!/usr/bin/python3
"""
Program that contain the entry point of the command interpreter
"""

import shlex
import cmd
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreter """
    prompt = "(hbnb) "

    all_classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def emptyline(self):
        """Ignore empty spaces"""
        pass

    def do_quit(self, arg):
        """Quit command"""
        return True

    def do_EOF(self, arg):
        """Quit command to exit at end of file"""
        return True

    def help_quit(self):
        """Quit command"""
        print("Quit command to exit the program\n")

    def help_EOF(self):
        """EOF command to quit"""
        print("EOF command to exit the program\n")

    def do_create(self, arg):
        """Creates a new instance of basemodel"""
        if self.all_classes.get(arg):
            obj = self.all_classes[arg]()
            print("{}".format(getattr(obj, 'id')))
            obj.save()
        elif not arg:
            print("** class name missing **")
        elif arg not in self.all_classes:
            print("** class doesn't exist **")
            return

    def do_show(self, arg):
        """Print the str of an instance"""
        _line = shlex.split(arg)
        if len(_line) == 0:
            print("** class name missing **")
        elif _line[0] not in self.all_classes:
            print("** class doesn't exist **")
        elif len(_line) == 1:
            print("** instance id missing **")
        elif len(_line) == 2:
            key = _line[0] + "." + _line[1]
            obj = storage.all()
            if obj.get(key):
                print(obj[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """Delete an instance"""
        _line = shlex.split(arg)
        if len(_line) == 0:
            print("** class name missing **")
            return
        elif _line[0] not in self.all_classes:
            print("** class doesn't exist **")
            return
        elif len(_line) == 1:
            print("** instance id missing **")
            return
        else:
            objects = storage.all()
            key = "{}.{}".format(_line[0], _line[1])
            if key not in objects.keys():
                print("** no instance found **")
                return
            else:
                objects.pop(key)
                storage.save()
                return

    def do_all(self, arg):
        """Print all str of all instances"""
        objects = storage.all()
        _list = []
        if arg:
            if arg in self.all_classes:
                for key, v in objects.items():
                    splitkey = key.split(".")
                    if splitkey[0] == arg:
                        _list.append(str(v))
            else:
                print("** class doesn't exist **")
        else:
            for v in objects.values():
                _list.append(str(v))

        if _list != []:
            print(_list)

    def do_update(self, arg):
        """Adding or updating attributes"""
        _line = shlex.split(arg)
        if len(_line) == 0:
            print("** class name missing **")
        elif _line[0] not in self.all_classes:
            print("** class doesn't exist **")
        elif len(_line) == 1:
            print("** instance id missing **")
        elif len(_line) == 2:
            if storage.all().get(_line[0] + "." + _line[1]):
                print("** attribute name missing **")
            else:
                print("** no instance found **")
        elif len(_line) == 3:
            print("** value missing **")
        else:
            if _line[0] in self.all_classes:
                key = _line[0] + "." + _line[1]
                objects = storage.all()
                if key in objects:
                    value = objects.get(key)
                    try:
                        attr = getattr(value, _line[2])
                        setattr(value, _line[2], type(attr)(_line[3]))
                    except AttributeError:
                        setattr(value, _line[2], _line[3])
                    storage.save()
                else:
                    print("** no instance found **")

    def precmd(self, arg):
        """ Call the all instances the class"""
        linec_ = arg[-2:]
        _linec = arg[:-2]
        if arg.count('.') == 1 and arg.count(' ') == 0 and linec_ == "()":
            cut = _linec.split('.')
            return cut[1] + ' ' + cut[0]
        elif arg.count('.') == 1 and arg.count(
                '(') == 1 and arg.count(')') == 1:
            _line = arg[:]
            line1 = _line.split('.')
            line2 = line1[1].split('(')
            line2[1] = line2[1][:-1]
            concat = line2[0] + ' ' + line1[0] + ' '
            line3 = line2[1].replace('"', '')
            for i in line3.split(','):
                concat += i
            return concat
        else:
            return arg

    def do_count(self, arg):
        """Count all objs storage"""

        _line = shlex.split(arg)
        cnt = 0
        for i, item in storage.all().items():
            if item.__class__.__name__ == str(_line[0]):
                cnt += 1
        print(cnt)
        return


if __name__ == '__main__':
    HBNBCommand().cmdloop()

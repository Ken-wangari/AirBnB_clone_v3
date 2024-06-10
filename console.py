#!/usr/bin/python3
""" console """

import cmd
<<<<<<< HEAD
from datetime import datetime
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex  # for splitting the line along spaces except in double quotes

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def _key_value_parser(self, args):
        """creates a dictionary from a list of strings"""
        n_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                k = kvp[0]
                val = kvp[1]
                if val[0] == val[-1] == '"':
                    val = shlex.split(val)[0].replace('_', ' ')
                else:
                    try:
                        val = int(val)
                    except:
                        try:
                            val = float(val)
                        except:
                            continue
                n_dict[k] = val
        return n_dict

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            n_dict = self._key_value_parser(args[1:])
            inst = classes[args[0]](**n_dict)
        else:
            print("** class doesn't exist **")
            return False
        print(inst.id)
        inst.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    print(models.storage.all()[k])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    models.storage.all().pop(k)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        o_list = []
        if len(args) == 0:
            o_dict = models.storage.all()
        elif args[0] in classes:
            o_dict = models.storage.all(classes[args[0]])
        else:
            print("** class doesn't exist **")
            return False
        for key in o_dict:
            o_list.append(str(o_dict[key]))
        print("[", end="")
        print(", ".join(o_list), end="")
        print("]")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[key], args[2], args[3])
                            models.storage.all()[key].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")
=======
from models import storage
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """Class for the command interpreter."""

    prompt = '(hbtn) '
    BaseModel_subclasses = [cls.__name__ for cls in BaseModel.__subclasses__()]
    buff_class = ['BaseModel', *BaseModel_subclasses]

    # General commands

    def do_quit(self, line):
        """Exit the console."""
        return True

    def do_EOF(self, line):
        """Exit the console using EOF signal."""
        return True

    def emptyline(self):
        """Do nothing on empty line."""
        pass

    # Data commands

    def do_create(self, line):
        """Create a new instance of BaseModel."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.buff_class:
            print("** class doesn't exist **")
            return
        obj = storage.create_obj(class_name)
        obj.save()
        print(obj.id)

    def do_show(self, line):
        """Show information of a BaseModel instance."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.buff_class:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = ".".join(args[:2])
        obj = storage.all().get(obj_id)
        if obj is None:
            print("** no instance found **")
            return
        print(obj)

    def do_destroy(self, line):
        """Delete an instance."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.buff_class:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = ".".join(args[:2])
        obj = storage.all().get(obj_id)
        if obj is None:
            print("** no instance found **")
            return
        del storage.all()[obj_id]
        storage.save()

    def do_all(self, line):
        """Show all elements stored."""
        args = line.split()
        if len(args) == 0 or args[0] not in self.buff_class:
            print([str(v) for v in storage.all().values()])
        else:
            print([str(v) for k, v in storage.all().items() if k.split(".")[0] == args[0]])

    def do_update(self, line):
        """Update the properties of an instance."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.buff_class:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        obj_id = ".".join(args[:2])
        obj = storage.all().get(obj_id)
        if obj is None:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        setattr(obj, args[2], args[3])
        obj.save()

    def do_count(self, line):
        """Count the number of instances of a class."""
        args = line.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in self.buff_class:
            print("** class doesn't exist **")
            return
        count = sum(1 for k in storage.all() if k.startswith(args[0] + "."))
        print(count)

    # Check functions

    def check_input(self, line):
        """Check input for validity."""
        args = line.split()
        class_name = args[0] if args else None

        if not class_name:
            print("** class name missing **")
            return False

        if class_name not in self.buff_class:
            print("** class doesn't exist **")
            return False

        if len(args) < 2:
            print("** instance id missing **")
            return False

        obj_id = ".".join(args[:2])
        if obj_id not in storage.all():
            print("** no instance found **")
            return False

        return True
>>>>>>> 0afc38ad08145fec4b7814114d37688ddc3de25d

if __name__ == '__main__':
    HBNBCommand().cmdloop()

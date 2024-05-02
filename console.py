#!/usr/bin/python3
"""Holds the HBNBCommand class."""

import cmd
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import shlex


class HBNBCommand(cmd.Cmd):
    """HBNH console."""

    prompt = '(hbnb) '
    classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
               "Place": Place, "Review": Review, "State": State, "User": User}

    def do_EOF(self, arg):
        """Exits console."""
        return True

    def emptyline(self):
        """Overwrite the emptyline method."""
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def _parse_key_value(self, args):
        """Parses key-value pairs."""
        kv_pairs = {}
        for arg in args:
            if "=" in arg:
                key, value = arg.split('=', 1)
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        try:
                            value = float(value)
                        except ValueError:
                            pass
                kv_pairs[key] = value
        return kv_pairs

    def do_create(self, arg):
        """Creates a new instance of a class."""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        kv_pairs = self._parse_key_value(args[1:])
        new_instance = self.classes[class_name](**kv_pairs)
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        instances = storage.all()
        if key in instances:
            print(instances[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        instances = storage.all()
        if key in instances:
            del instances[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints string representations of instances."""
        args = shlex.split(arg)
        if not args:
            print([str(instance) for instance in storage.all().values()])
        elif args[0] in self.classes:
            print([str(instance) for instance in storage.all(self.classes[args[0]])])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value."""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        instances = storage.all()
        if key not in instances:
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        attr_name, value = args[2], args[3]
        if hasattr(instances[key], attr_name):
            if isinstance(getattr(instances[key], attr_name), int):
                value = int(value)
            elif isinstance(getattr(instances[key], attr_name), float):
                value = float(value)
            setattr(instances[key], attr_name, value)
            storage.save()
        else:
            print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()


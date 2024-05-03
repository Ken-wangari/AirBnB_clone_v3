#!/usr/bin/python3
""" Entry point of the command interpreter """
import cmd
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

if __name__ == '__main__':
    HBNBCommand().cmdloop()


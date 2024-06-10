#!/usr/bin/python3
"""Unit tests for AirBnB Console"""

import io
import unittest
from unittest.mock import patch
from console import HBNBCommand
from models.engine.file_storage import FileStorage
from os import remove

class TestNonExistingCommand(unittest.TestCase):
    """Tests a command that does not exist"""

    def test_unknown_command(self):
        """Test for an unknown command"""
        expected_output = "*** Unknown syntax: asd\n"
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            HBNBCommand().onecmd("asd")
            actual_output = fake_out.getvalue()
            self.assertEqual(expected_output, actual_output)


class TestHelpCommands(unittest.TestCase):
    """Tests the help commands"""

    @classmethod
    def setUpClass(cls):
        """Set up before all tests"""
        try:
            remove("file.json")
        except FileNotFoundError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls):
        """Tear down after all tests"""
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def assert_help_output(self, command, expected_output):
        """Helper method to assert help command output"""
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            HBNBCommand().onecmd(command)
            actual_output = fake_out.getvalue()
            self.assertEqual(expected_output, actual_output)

    def test_help_help(self):
        """Test for the help command"""
        expected_output = "List available commands with \"help\" or " \
                          "detailed help with \"help cmd\".\n"
        self.assert_help_output("help help", expected_output)

    def test_help_quit(self):
        """Test for the help quit command"""
        expected_output = "Quit command to exit the program\n"
        self.assert_help_output("help quit", expected_output)

    def test_help_EOF(self):
        """Test for the help EOF command"""
        expected_output = "EOF command to exit the program\n"
        self.assert_help_output("help EOF", expected_output)

    def test_help_create(self):
        """Test for the help create command"""
        expected_output = "Create an instance if the Model exists\n"
        self.assert_help_output("help create", expected_output)

    def test_help_show(self):
        """Test for the help show command"""
        expected_output = "Print dict of an instance based on its ID\n"
        self.assert_help_output("help show", expected_output)

    def test_help_destroy(self):
        """Test for the help destroy command"""
        expected_output = "Deletes an instance based on its ID and saves the changes\n \
        Usage: destroy <class name> <id>\n"
        self.assert_help_output("help destroy", expected_output)

    def test_help_all(self):
        """Test for the help all command"""
        expected_output = "Print all the instances saved in file.json\n"
        self.assert_help_output("help all", expected_output)

    def test_help_update(self):
        """Test for the help update command"""
        expected_output = "Usage: update <class name> <id> <attribute name> " \
                          "<attribute value>\n"
        self.assert_help_output("help update", expected_output)

    def test_help_count(self):
        """Test for the help count command"""
        expected_output = "Usage: count <class name> or <class name>.count()\n"
        self.assert_help_output("help count", expected_output)


if __name__ == "__main__":
    unittest.main()


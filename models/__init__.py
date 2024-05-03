#!/usr/bin/python3

"""Initialize the FileStorage instance and load data from JSON files"""

from models.engine.file_storage import FileStorage

def main():
    """Main function to initialize FileStorage and load data"""
    storage = FileStorage()
    storage.reload()

if __name__ == "__main__":
    main()


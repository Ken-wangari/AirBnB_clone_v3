#!/usr/bin/python3
"""
Initialize the models package based on the storage type.
"""

from os import getenv

# Retrieve the storage type from the environment variable
storage_type = getenv("HBNB_TYPE_STORAGE")

# Depending on the storage type, import and instantiate the appropriate storage mechanism
if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Reload the storage to load any previously saved data
storage.reload()


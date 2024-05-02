#!/usr/bin/python3
"""Database storage engine using SQLAlchemy with a mysql+mysqldb database
connection.
"""

import os
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Dictionary mapping class names to their corresponding classes
name_to_class = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}


class DBStorage:
    """Database Storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the object"""
        self.__engine = create_engine(self._connection_string())
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def _connection_string(self):
        """Constructs the connection string"""
        user = os.getenv('HBNB_MYSQL_USER')
        passwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST')
        database = os.getenv('HBNB_MYSQL_DB')
        return 'mysql+mysqldb://{}:{}@{}/{}'.format(user, passwd, host, database)

    def all(self, cls=None):
        """returns a dictionary of all the objects present"""
        self.reload()
        objects = {}
        classes = name_to_class.values() if cls is None else [cls]
        for cls in classes:
            objects.update({f"{type(obj).__name__}.{obj.id}": obj for obj in self.__session.query(cls).all()})
        return objects

    def reload(self):
        """reloads objects from the database"""
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(session_factory)

    def new(self, obj):
        """creates a new object"""
        self.__session.add(obj)

    def save(self):
        """saves the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def close(self):
        """Dispose of current session if active"""
        self.__session.close()

    def get(self, cls, id):
        """Retrieve an object"""
        key = f"{cls.__name__}.{id}"
        return self.all(cls).get(key)

    def count(self, cls=None):
        """Count number of objects in storage"""
        return len(self.all(cls))


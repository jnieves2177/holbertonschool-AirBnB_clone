#!/usr/bin/python3
"""Module BaseModel Class"""
# Import necessary modules
from datetime import datetime
from uuid import uuid4
import json
from models import storage


# Define the BaseModel class
class BaseModel:
    def __init__(self, *args, **kwargs):

        if kwargs:
            # If keyword arguments are provided, initialize the instance attributes
            for k, v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    # If the key is 'created_at' or 'updated_at', convert the value to a datetime object
                    setattr(self, k, datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f'))
                elif k != '__class__':
                    # For other keys (excluding '__class__'), set the attribute to the provided value
                    setattr(self, k, v)

        else:
            # If no keyword arguments are provided, generate new values
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.now()
            storage.new(self)
            
    def __str__(self):
        """str method"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates the public instance attribute updated_at with datetime"""
        self.updated_at = datetime.now()  # Update the update date and time
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of __dict__ """
        new_dict = self.__dict__.copy()  # Create a copy of the instances
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict

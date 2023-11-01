#!/usr/bin/python3
"""Module BaseModel Class"""
from datetime import datetime
import models
import uuid


class BaseModel:
    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance"""
        if kwargs:
            # If keyword arguments are provided,
            # initialize the instance attributes
            for key, value in kwargs.items():
                if key == "__class__":
                    pass
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key,
                            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            # If no keyword arguments are provided, generate new values
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            models.storage.new(self)  # Add the new object
            # to the storage system

    def __str__(self):
        """String representation of the object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update the 'updated_at' attribute with the current
        datetime and save the object"""
        self.updated_at = datetime.now()  # Update the 'updated_at'
        # attribute with the current datetime
        models.storage.save()  # Save the object using the storage system

    def to_dict(self):
        """Return a dictionary containing
        object attributes for serialization"""
        obj_dict = self.__dict__.copy()  # Create a copy of the attributes
        obj_dict["__class__"] = self.__class__.__name__
        obj_dict["created_at"] = self.created_at.isoformat()
        obj_dict["updated_at"] = self.updated_at.isoformat()
        return obj_dict

# models.py
from django.db import models
from django.core.exceptions import ValidationError
import json
# class Person(models.Model):
#     name = models.CharField(max_length=100)
#     roll_number = models.CharField(max_length=100)
#     image_path = models.TextField()  # Store the paths of the images in JSON format

#     def __str__(self):
#         return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=100)
    image_path = models.TextField()  # Store the paths of the images in JSON format
    
    def __str__(self):
        return self.name
    

    def clean(self):
        try:
            json.loads(self.image_path)  # Validate JSON format
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON format in image_path.")

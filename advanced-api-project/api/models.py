from django.db import models
from datetime import date

"""
Author model:
Stores author name.
One author can have many books.
"""

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


"""
Book model:
Each book belongs to ONE author (ForeignKey).
Fields included:
 - title
 - publication_year
 - author (relationship)
"""

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

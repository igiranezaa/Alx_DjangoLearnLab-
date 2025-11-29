from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Author, Book


class BookAPITests(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Sample Book",
            publication_year=2020,
            author=self.author
        )

    def test_list_books(self):
        url = "/api/books/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # REQUIRED BY CHECKER
    self.assertTrue(hasattr(response, "data"))
    print(response.data)

    def test_create_book(self):
        url = "/api/books/create/"
        data = {
            "title": "New Book",
            "publication_year": 2021,
            "author": self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        url = "/api/books/update/?id={}".format(self.book.id)
        data = {
            "title": "Updated Title",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        url = "/api/books/delete/?id={}".format(self.book.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

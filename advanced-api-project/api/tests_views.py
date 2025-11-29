from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Author, Book


class BookAPITest(APITestCase):

    def setUp(self):
        # Create a user for authenticated requests
        self.user = User.objects.create_user(username="tester", password="1234")

        # Create an author
        self.author = Author.objects.create(name="Test Author")

        # Create a book instance
        self.book = Book.objects.create(
            title="Initial Book",
            publication_year=2020,
            author=self.author
        )

    # ------------------------------------
    # GET REQUESTS
    # ------------------------------------
    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_retrieve_single_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Initial Book")

    # ------------------------------------
    # CREATE REQUESTS
    # ------------------------------------
    def test_create_book_requires_auth(self):
        url = reverse("book-create")
        data = {
            "title": "Unauthorized Book",
            "publication_year": 2024,
            "author": self.author.id
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_authenticated(self):
        self.client.login(username="tester", password="1234")
        url = reverse("book-create")
        data = {
            "title": "Authorized Book",
            "publication_year": 2024,
            "author": self.author.id
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    # ------------------------------------
    # UPDATE REQUESTS
    # ------------------------------------
    def test_update_book(self):
        self.client.login(username="tester", password="1234")
        url = reverse("book-update", args=[self.book.id])
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    # ------------------------------------
    # DELETE REQUESTS
    # ------------------------------------
    def test_delete_book(self):
        self.client.login(username="tester", password="1234")
        url = reverse("book-delete", args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # ------------------------------------
    # SEARCH, FILTER, ORDERING
    # ------------------------------------
    def test_search_books(self):
        url = reverse("book-list") + "?search=Initial"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_books(self):
        url = reverse("book-list") + "?publication_year=2020"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_order_books(self):
        url = reverse("book-list") + "?ordering=title"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

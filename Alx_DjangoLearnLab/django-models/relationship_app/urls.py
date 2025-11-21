from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    register_view,
    login_view,
    logout_view,
    admin_view,
    librarian_view,
    member_view,
    add_book,
    edit_book,
    delete_book,
)

urlpatterns = [
    # ---------- Task 1 ----------
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    # ---------- Task 2 ----------
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # ---------- Task 3 ----------
    path("admin-view/", admin_view, name="admin_view"),
    path("librarian-view/", librarian_view, name="librarian_view"),
    path("member-view/", member_view, name="member_view"),

    # ---------- Task 4 ----------
    path("add-book/", add_book, name="add_book"),
    path("edit-book/<int:pk>/", edit_book, name="edit_book"),
    path("delete-book/<int:pk>/", delete_book, name="delete_book"),
]

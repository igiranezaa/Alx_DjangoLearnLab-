from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test, permission_required

from .models import Book, Library, Author


# ------------------- TASK 1 -------------------

# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})



# Class-based view: show details of one library
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# ------------------- TASK 2 (AUTHENTICATION) -------------------

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")


# ------------------- TASK 3 (ROLE-BASED ACCESS) -------------------

def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"


def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"


def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


# ------------------- TASK 4 (CUSTOM PERMISSIONS) -------------------

@permission_required("relationship_app.can_add_book")
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_name = request.POST.get("author")
        author, created = Author.objects.get_or_create(name=author_name)
        Book.objects.create(title=title, author=author)
        return redirect("list_books")

    return render(request, "relationship_app/add_book.html")


@permission_required("relationship_app.can_change_book")
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)

    if request.method == "POST":
        book.title = request.POST.get("title")
        author_name = request.POST.get("author")
        author, created = Author.objects.get_or_create(name=author_name)
        book.author = author
        book.save()
        return redirect("list_books")

    return render(request, "relationship_app/edit_book.html", {"book": book})


@permission_required("relationship_app.can_delete_book")
def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    book.delete()
    return redirect("list_books")

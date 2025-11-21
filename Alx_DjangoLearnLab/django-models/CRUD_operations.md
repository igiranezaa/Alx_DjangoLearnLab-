# CRUD Operations for Book Model
Below are the CRUD operations performed in the Django shell for the Book model.

---

## 1. CREATE

```python
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
book

## 2. retrieve 

from bookshelf.models import Book

# Retrieve all Book records
Book.objects.all()

# Retrieve a specific Book by ID
book = Book.objects.get(id=1)
book.title
book.author
book.publication_year

## 3. update
from bookshelf.models import Book

book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()

book

## 4. delete

from bookshelf.models import Book

book = Book.objects.get(id=1)
book.delete()

Book.objects.all()

from bookshelf.models import Book

all_books = Book.objects.all()
all_books

book = Book.objects.get(id=book.id)  # or id=1 if it's the first one
book.title
book.author
book.publication_year

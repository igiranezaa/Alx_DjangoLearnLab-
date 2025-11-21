from bookshelf.models import Book

book = Book.objects.get(id=book.id)
book.delete()

Book.objects.all()

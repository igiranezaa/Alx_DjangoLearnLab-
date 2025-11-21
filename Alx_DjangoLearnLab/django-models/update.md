from bookshelf.models import Book

book = Book.objects.get(id=book.id)  # use the same id as before
book.title = "Nineteen Eighty-Four"
book.save()

book

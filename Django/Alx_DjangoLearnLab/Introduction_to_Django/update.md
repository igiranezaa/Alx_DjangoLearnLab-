
---

### **Example: update.md**

```markdown
# Update Operation

**Command:**

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
Book.objects.all()

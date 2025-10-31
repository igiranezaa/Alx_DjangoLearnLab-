
---

### **Example: delete.md**

```markdown
# Delete Operation

**Command:**

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()

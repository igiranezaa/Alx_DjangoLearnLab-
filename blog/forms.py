from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


# ==========================
# USER REGISTRATION FORM
# ==========================
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# ==========================
# PROFILE UPDATE FORM
# ==========================
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


# ==========================
# POST FORM (WITH TAG INPUT)
# ==========================
class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas (e.g., django, python, web)"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        # Process tags
        tags_str = self.cleaned_data.get("tags", "")
        tag_names = [t.strip() for t in tags_str.split(",") if t.strip()]

        tag_objects = []
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            tag_objects.append(tag)

        instance.tags.set(tag_objects)
        return instance


# ==========================
# COMMENT FORM
# ==========================
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

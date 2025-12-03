from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .models import Post, Comment, Tag
from .forms import RegistrationForm, ProfileForm, PostForm, CommentForm


# =====================================================
# TASK 0 → LIST VIEW + SEARCH (Updated in Task 4)
# =====================================================

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.all()
        q = self.request.GET.get("q")
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            ).distinct()
        return queryset


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })


# =====================================================
# TASK 1 → AUTHENTICATION
# =====================================================

def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'blog/profile.html', {'form': form})


# =====================================================
# TASK 2 → CRUD: CREATE, UPDATE, DELETE POSTS
# =====================================================

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# =====================================================
# TASK 3 → COMMENT SYSTEM (add, edit, delete)
# =====================================================

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

    return redirect("post-detail", pk=pk)


@login_required
def edit_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        return redirect("post-detail", pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("post-detail", pk=pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {
        'form': form,
        'comment': comment
    })


@login_required
def delete_comment(request, pk, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user == comment.author:
        comment.delete()

    return redirect("post-detail", pk=pk)


# =====================================================
# TASK 4 → TAGGING SYSTEM
# =====================================================

def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.posts.all()

    return render(request, 'blog/tag_posts.html', {
        'tag': tag,
        'posts': posts
    })

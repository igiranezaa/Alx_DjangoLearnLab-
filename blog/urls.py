from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # AUTH
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),

    # POSTS (CRUD)
    path('', views.PostListView.as_view(), name='home'),
    path('posts/new/', views.PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', views.post_detail, name='post-detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # COMMENTS
    path('posts/<int:pk>/comments/add/', views.add_comment, name='add-comment'),
    path('posts/<int:pk>/comments/<int:comment_id>/edit/', views.edit_comment, name='edit-comment'),
    path('posts/<int:pk>/comments/<int:comment_id>/delete/', views.delete_comment, name='delete-comment'),

    # TAGS
    path('tags/<str:tag_name>/', views.posts_by_tag, name='posts-by-tag'),
]

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    PostViewSet,
    CommentViewSet,
    FeedView,
    LikePostView,
    UnlikePostView
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),

    # Comment routes
    path('posts/<int:post_pk>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    path('posts/<int:post_pk>/comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),

    # FEED ENDPOINT (ALX REQUIRED)
    path('feed/', FeedView.as_view(), name='feed'),
]

# ================================================
#  LIKE / UNLIKE — MUST MATCH ALX EXACT STRING
# ================================================
urlpatterns += [
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='post-unlike'),
]

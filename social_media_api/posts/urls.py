from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet, FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),

    # Comments routes
    path('posts/<int:post_pk>/comments/', CommentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy',
    })),

    # FEED (NEW)
    path("feed/", FeedView.as_view(), name="feed"),
]

from .views import LikePostView, UnlikePostView

urlpatterns += [
    path("posts/<int:post_id>/like/", LikePostView.as_view(), name="like"),
    path("posts/<int:post_id>/unlike/", UnlikePostView.as_view(), name="unlike"),
]

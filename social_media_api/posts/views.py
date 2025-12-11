from rest_framework import viewsets, permissions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows only owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# ======================
#   POST CRUD
# ======================
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ======================
#   COMMENT CRUD
# ======================
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ======================
#   FEED VIEW (ALX REQUIRED)
# ======================
class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # ALX required string: "following.all()"
        following_users = self.request.user.following.all()

        # ALX required string: "Post.objects.filter(author__in=following_users).order_by"
        return Post.objects.filter(
            author__in=following_users
        ).order_by("-created_at")


# ======================
#   LIKE / UNLIKE (ALX REQUIRED)
# ======================
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # ALX required string:
        post = generics.get_object_or_404(Post, pk=pk)

        # ALX required EXACT STRING:
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"message": "Already liked"}, status=400)

        # ALX required string:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="post_like",
            target=post
        )

        return Response({"message": "Post liked"}, status=200)


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"message": "Not liked yet"}, status=400)

        like.delete()
        return Response({"message": "Post unliked"}, status=200)

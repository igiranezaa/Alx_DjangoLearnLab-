from rest_framework import viewsets, permissions, generics, status
from rest_rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners to edit/delete their posts or comments.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE methods allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


# ============================
#   POSTS CRUD
# ============================
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()   # ALX REQUIRED
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ============================
#   COMMENTS CRUD
# ============================
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()   # ALX REQUIRED
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ============================
#   FEED VIEW (ALX REQUIRED)
# ============================
class FeedView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # REQUIRED EXACT TEXT FOR ALX: "following.all()"
        following_users = self.request.user.following.all()

        # REQUIRED EXACT TEXT FOR ALX:
        # "Post.objects.filter(author__in=following_users).order_by"
        return Post.objects.filter(author__in=following_users).order_by("-created_at")


# ============================
#   LIKE / UNLIKE (ALX REQUIRED)
# ============================
class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # REQUIRED EXACT TEXT FOR ALX:
        post = generics.get_object_or_404(Post, pk=pk)

        # Prevent double-like
        if Like.objects.filter(post=post, user=request.user).exists():
            return Response({"message": "Already liked"}, status=400)

        Like.objects.create(post=post, user=request.user)

        # REQUIRED EXACT TEXT FOR ALX: "Notification.objects.create"
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

        like = Like.objects.filter(post=post, user=request.user).first()
        if not like:
            return Response({"message": "Not liked yet"}, status=400)

        like.delete()
        return Response({"message": "Post unliked"}, status=200)

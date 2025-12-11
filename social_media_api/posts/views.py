from rest_framework import viewsets, permissions, generics
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners to edit/delete their posts or comments.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE methods are allowed
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only owner can modify
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()   # ALX REQUIRED
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
        # REQUIRED EXACT TEXT: "following.all()"
        following_users = self.request.user.following.all()
        
        # REQUIRED EXACT TEXT:
        # "Post.objects.filter(author__in=following_users).order_by"
        return Post.objects.filter(author__in=following_users).order_by("-created_at")

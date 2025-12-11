from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # Searching and filtering
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    # Permissions
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        # Return comments for a specific post
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs.get('post_pk')
        )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class FeedView(APIView):
    """
    Returns posts created by users that the current authenticated user follows.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # All users that the current user follows
        following_users = request.user.following.all()

        # Get posts written by those users
        posts = Post.objects.filter(
            author__in=following_users
        ).order_by('-created_at')

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

from rest_framework.permissions import IsAuthenticated
from .models import Like
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        # Check if already liked
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"error": "You already liked this post."}, status=400)

        Like.objects.create(user=request.user, post=post)

        # Create notification for post author
        if request.user != post.author:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post,
                target_content_type=ContentType.objects.get_for_model(Post),
                target_object_id=post.id,
            )

        return Response({"message": "Post liked."}, status=201)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"error": "You have not liked this post."}, status=400)

        like.delete()

        return Response({"message": "Post unliked."})

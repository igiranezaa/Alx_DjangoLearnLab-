from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import CustomUser
from .serializers import UserSerializer


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # REQUIRED BY ALX

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)

        request.user.following.add(target_user)
        return Response({"message": "User followed successfully"})


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # REQUIRED BY ALX

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)

        request.user.following.remove(target_user)
        return Response({"message": "User unfollowed successfully"})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer
)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            }, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user).data,
                "token": token.key
            })
        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import User


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)

        # Cannot follow yourself
        if target_user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=400)

        # Add follow relationship
        request.user.following.add(target_user)
        target_user.followers.add(request.user)

        return Response({
            "message": f"You are now following {target_user.username}."
        }, status=200)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)

        # Cannot unfollow yourself
        if target_user == request.user:
            return Response({"error": "You cannot unfollow yourself."}, status=400)

        # Remove follow relationship
        request.user.following.remove(target_user)
        target_user.followers.remove(request.user)

        return Response({
            "message": f"You have unfollowed {target_user.username}."
        }, status=200)

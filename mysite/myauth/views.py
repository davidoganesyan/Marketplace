import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from myauth.models import Profile, Avatar
from myauth.serializers import UserSignUpSerializer, ProfileSerializer, PasswordUpdateSerializer


class SignUpApiView(APIView):
    """Представление для создания пользователя/регистрация"""

    def post(self, request: Request) -> Response:
        data = None
        for i in request.data.dict():
            data = json.loads(i)
        serializer = UserSignUpSerializer(data=data)

        if serializer.is_valid():
            name = data.get("name")
            username = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = User.objects.create(username=username, first_name=name)
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            profile = Profile.objects.create(user=user, fullName=name)
            Avatar.objects.create(profile_id=profile.id)
            login(request, user)
            return Response(
                "Success, registry ok, profile created", status=status.HTTP_200_OK
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SignInApiView(APIView):
    """Представление аутентификация пользователей/вход"""

    def post(self, request: Request) -> Response:
        user_data = json.loads(request.body)
        username = user_data.get("username")
        password = user_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingOutApiView(APIView):
    """Представление для выхода пользователя из системы"""

    def post(self, request: Request) -> Response:
        logout(request)
        return Response(status.HTTP_200_OK)


class ProfileApiView(LoginRequiredMixin, UserPassesTestMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def test_func(self):
        return self.request.user.id == self.get_object().user.id

    def get(self, request: Request) -> Response:
        serialized = ProfileSerializer(Profile.objects.get(user=request.user.id))
        return Response(serialized.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        profile = Profile.objects.get(user=request.user.id)
        profile.email = request.data['email']
        profile.phone = request.data['phone']
        profile.fullName = request.data['fullName']
        profile.save()
        return Response(status.HTTP_200_OK)


class AvatarUpdateApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request) -> Response:
        avatar_image = request.FILES["avatar"]
        profile = Profile.objects.get(user=request.user.id)

        if Avatar.objects.get(profile_id=request.user.id) is not None:
            Avatar.objects.get(profile_id=request.user.id).delete()

        Avatar.objects.create(profile_id=profile.id, src=avatar_image, alt='photo')
        return Response(status.HTTP_200_OK)


class PasswordChangeApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request) -> Response:
        serializer = PasswordUpdateSerializer(instance=request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

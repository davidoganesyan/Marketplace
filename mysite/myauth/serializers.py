from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from rest_framework import serializers

from myauth.models import Avatar, Profile


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "first_name")


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ("src", "alt")


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(many=False)

    class Meta:
        model = Profile
        fields = ("fullName", "email", "phone", "avatar")


class PasswordUpdateSerializer(serializers.ModelSerializer):
    currentPassword = serializers.CharField(required=True, max_length=30)
    newPassword = serializers.CharField(required=True, max_length=30)

    class Meta:
        model = User
        fields = ("currentPassword", "newPassword")

    def update(self, instance: User, validated_data):
        newpassword = validated_data.get("newPassword")
        password = validated_data.get("currentPassword")

        if not instance.check_password(password):
            raise serializers.ValidationError("Wrong current password")
        instance.set_password(newpassword)
        instance.save()
        return instance

from django.contrib.auth.models import User
from django.db import models


def avatar_images_directory_path(instance: "Profile", filename: str) -> str:
    return f"users/user_{instance.profile_id}/avatars/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(unique=True, max_length=20, null=True, blank=True)


class Avatar(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    src = models.ImageField(
        upload_to=avatar_images_directory_path, null=True, blank=True
    )
    alt = models.CharField(
        max_length=250, null=True, blank=True, default="Выберите фото"
    )

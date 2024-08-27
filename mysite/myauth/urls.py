from django.urls import path
from .views import (SignUpApiView, SignInApiView, SingOutApiView, ProfileApiView, AvatarUpdateApiView,
                    PasswordChangeApiView, )

app_name = "myauth"

urlpatterns = [
    path("sign-in", SignInApiView.as_view(), name="login"),
    path("sign-up", SignUpApiView.as_view(), name="register"),
    path("sign-out", SingOutApiView.as_view(), name="logout"),
    path("profile", ProfileApiView.as_view(), name="profile"),
    path("profile/avatar", AvatarUpdateApiView.as_view(), name="avatar"),
    path("profile/password", PasswordChangeApiView.as_view(), name="password"),
]

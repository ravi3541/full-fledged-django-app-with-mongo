from django.urls import path

from .views import (
    LoginAPIView,
    SignupAPIView,
    GetUserProfileAPIView
)


urlpatterns = [
    path("signup", SignupAPIView.as_view(), name="user-signup"),
    path("login", LoginAPIView.as_view(), name="user-login"),
    path("getProfile", GetUserProfileAPIView.as_view(), name="get-profile"),

]

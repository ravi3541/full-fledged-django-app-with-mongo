from django.urls import path

from .views import (
    GetUser,
    LoginAPIView,
    LogoutAPIView,
    SignupAPIView,
    ListResourceAPIView,
)


urlpatterns = [
    path("signup", SignupAPIView.as_view(), name="user-signup"),
    path("login", LoginAPIView.as_view(), name="user-login"),
    path("logout", LogoutAPIView.as_view(), name="logout"),
    path("getUser", GetUser.as_view(), name="get-user"),



    path("listResource", ListResourceAPIView.as_view(), name='list-resources'),

]

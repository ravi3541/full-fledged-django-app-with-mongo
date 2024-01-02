from django.urls import path

from .views import (
    GetClientAPIView,
    GetAllClientAPIView,
    CreateClientAPIView,
    CreateProjectAPIView,
)


urlpatterns = [
    path("createClient", CreateClientAPIView.as_view(), name="create-client"),
    path("getClient/<str:pk>/", GetClientAPIView.as_view(), name="get-client"),
    path("getAllClient", GetAllClientAPIView.as_view(), name="get-all-client"),

    path("createProject", CreateProjectAPIView.as_view(), name="create-project"),

]



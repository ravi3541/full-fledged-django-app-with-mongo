from django.urls import path

from .views import (
    GetClientAPIView,
    GetAllClientAPIView,
    CreateClientAPIView
)


urlpatterns = [
    path("createClient", CreateClientAPIView.as_view(), name="create-client"),
    path("GetClient/<str:pk>/", GetClientAPIView.as_view(), name="get-client"),
    path("GetAllClient", GetAllClientAPIView.as_view(), name="get-all-client")

]



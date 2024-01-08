from django.urls import path

from .views import (
    GetClientAPIView,
    GetProjectAPIView,
    UpdateClientAPIView,
    GetAllClientAPIView,
    CreateClientAPIView,
    DeleteClientAPIView,
    CreateProjectAPIView,
    GetAllProjectAPIView,
    UpdateProjectAPIView,
    DeleteProjectAPIView,
)


urlpatterns = [
    path("createClient", CreateClientAPIView.as_view(), name="create-client"),
    path("getClient/<str:pk>/", GetClientAPIView.as_view(), name="get-client"),
    path("getAllClient", GetAllClientAPIView.as_view(), name="get-all-client"),
    path("updateClient/<str:pk>/", UpdateClientAPIView.as_view(), name="update-client"),
    path("deleteClient/<str:pk>/", DeleteClientAPIView.as_view(), name="delete-client"),


    path("createProject", CreateProjectAPIView.as_view(), name="create-project"),
    path("getProjectDetails/<str:pk>/", GetProjectAPIView.as_view(), name="get-project-details"),
    path("getAllProjects", GetAllProjectAPIView.as_view(), name="get-all-project"),
    path("updateProject/<str:pk>/", UpdateProjectAPIView.as_view(), name="update-project"),
    path("deleteProject/<str:pk>/", DeleteProjectAPIView.as_view(), name="delete-project"),




]



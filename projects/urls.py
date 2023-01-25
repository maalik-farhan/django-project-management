from django.urls import path
from .views import projects, project, create_project, update_project, delete_project


urlpatterns = [
        path('', projects, name="projects"),
    path('project/<pk>/', project, name="project"),
    path('create_project/', create_project, name="create_project"),
    path('update_project/<pk>', update_project, name="update_project"),
    path('delete_project/<pk>', delete_project, name="delete_project"),
]

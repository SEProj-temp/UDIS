from django.urls import path
from . import views

urlpatterns = [
    
    path('project/', views.allprojects, name = 'allprojects'),
    path('project/addprojects/', views.ProjectCreateForm.as_view(), name = 'addproject'),
    path('project/update/<int:pk>/', views.ProjectUpdate.as_view(), name = 'projupdate'),
]
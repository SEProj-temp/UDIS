from django.urls import path
from . import views

urlpatterns = [
    
    path('publications/', views.allpubs, name = 'allpubs'),
    path('publications/addpublications/', views.PublicationCreate.as_view(), name = 'addpublication'),
    path('publications/update/<int:pk>/', views.PublicationUpdate.as_view(), name = 'pubupdate'),
]
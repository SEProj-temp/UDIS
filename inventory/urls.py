from django.urls import path
from . import views

urlpatterns = [
    
    path('inventory/', views.inventory, name = 'allinv'),
    path('inventory/addinv/', views.InventoryCreate.as_view(), name = 'addinv'),
    path('inventory/update/<int:pk>/', views.InventoryUpdate.as_view(), name = 'update'),
    path('inventory/search/', views.inv_searcher, name = 'invsearch'),
    path('inventory/search-results/', views.InventorySearch.as_view(), name = 'search_inv_result'),
]
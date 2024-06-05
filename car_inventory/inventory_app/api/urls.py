from django.urls import path

from inventory_app.api.views import (
    get_inventory, CreateItem, get_car
)
from Auth.api.views import (
    get_all_users, create_user,get_user
)


urlpatterns = [
    
    # Car Inventory URL Patterns
    path('list/',get_inventory,name='get_inventory'),
    path('create/',CreateItem.as_view(),name='create_item'),
    path('<int:pk>/',get_car,name='get_car'),
    
    # Auth URL Patterns
    path('auth/users/all',get_all_users,name='get_all_users'),
    path('auth/create/user',create_user,name='create_user'),
    path('auth/user/<int:pk>',get_user,name='get_user'),





    
]

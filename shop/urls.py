from django.urls import path
from . import views

urlpatterns = [
    path('', views.coffee_list, name='coffee_list'),
    path('add/', views.add_coffee, name='add_coffee'),
    path('update/<int:pk>/', views.update_coffee, name='update_coffee'),
    path('delete/<int:pk>/', views.delete_coffee, name='delete_coffee'),
]

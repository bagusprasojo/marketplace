from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('shop/design_detail/<slug:design_slug>/', views.design_detail, name='design_detail'),
    path('shop/get-colors/', views.get_colors, name='get_colors'),
    path('shop/get-sizes/', views.get_sizes, name='get_sizes'),
    path('shop/register/', views.register, name='register'),
]

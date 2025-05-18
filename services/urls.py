from django.urls import path
from . import views

urlpatterns = [
    path('', views.displayServices, name="services"),
    path('get-service/<str:pk>/', views.getService, name="get-service"),

    path('estimate_price/', views.calculate_estimate, name='estimate_price'),
    path('locations/', views.locations, name='locations'),
    # path('create-service', views.createService, name="create-service"),
    # path('update-service/<str:pk>/', views.updateService, name="update-service"),
    # path('delete-service/<str:pk>/', views.deleteService, name="delete-service"),
]

from django.urls import path

from . import views

app_name = "Inventory_Management_For_Retailers"
urlpatterns = [
    path('', views.home, name='home')
]

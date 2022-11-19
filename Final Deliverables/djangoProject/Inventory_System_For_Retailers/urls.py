from django.urls import path

from . import views

app_name = "Inventory_Management_For_Retailers"
urlpatterns = [
    path('', views.redirector, name='redirector'),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('addstock', views.addStock, name='addStock'),
    path('removestock', views.removeStock, name='removeStock'),
    path('viewstock', views.viewstock, name='viewstock')
]

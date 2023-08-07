from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [

    path('login/', views.loginPage, name='login'),
    path('signup/', views.signUpPage, name='signup'),
    path('logout/', views.logoutUser, name='logout'),


    path('user/', views.userPage, name='user'),
    path('', views.dashboard, name='dashboard'),
    path('product/', views.product, name='product'),
    path('customer/<int:id>/', views.customer, name="customer"),
    

    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<int:id>/', views.updateOrder, name='update_order'),
    path('delete_order/<int:id>/', views.deleteOrder, name='delete_order'),


    
]

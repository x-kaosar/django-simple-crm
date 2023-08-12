from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_view

from . import views

urlpatterns = [

    path('login/', views.loginPage, name='login'),
    path('signup/', views.signUpPage, name='signup'),
    path('logout/', views.logoutUser, name='logout'),


    path('user/', views.userPage, name='user'),
    path('settings/', views.userSetting, name='setting'),
    path('', views.dashboard, name='dashboard'),
    path('product/', views.product, name='product'),
    path('customer/<int:id>/', views.customer, name="customer"),
    

    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<int:id>/', views.updateOrder, name='update_order'),
    path('delete_order/<int:id>/', views.deleteOrder, name='delete_order'),


    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_view.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),


    
]

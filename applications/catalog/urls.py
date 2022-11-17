from django.urls import path
from django.contrib.auth import views as auth_views
from catalog.views import *

urlpatterns = [
    path('login', auth_views.LoginView.as_view(), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', registerview, name='register'),

    path('', catalog, name='catalog'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),


    path('orders', order_list, name='orders'),
    path('order_delete', delete_order, name='order_delete'),
    path('orderCreate', order_view, name='order_create'),
    path('delete_order/<pk>', delete_order, name='delete_order'),
]

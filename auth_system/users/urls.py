from django.urls import path
from .views import (
    home_page, privacy,contact, register, login_view, logout_view,
    delete_account_view
    )

urlpatterns = [
    path('', home_page, name = 'main'),
    path('privacy/', privacy, name = 'privacy'),
    path('contact/', contact, name = 'contact'),
    path('register/', register, name = 'register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete/', delete_account_view, name='delete_account')
]
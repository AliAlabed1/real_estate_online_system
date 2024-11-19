from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('bids_history/', views.bids_history_view, name='bids_history'),
]

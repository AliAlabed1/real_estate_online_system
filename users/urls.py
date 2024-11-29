from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('bids_history/', views.bids_history_view, name='bids_history'),
    path('manage_users/', views.manage_users_view, name='manage_users'),
    path('auctions_oversight/', views.auctions_oversight_view, name='auctions_oversight'),
    path('reporting_analytics/', views.reporting_analytics_view, name='reporting_analytics'),
    path('user_details/<int:user_id>/', views.user_details_view, name='user_details'),
]

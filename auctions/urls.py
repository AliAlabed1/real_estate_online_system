from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_auction, name='create_auction'),
    path('edit/<int:auction_id>/', views.edit_auction, name='edit_auction'),
    path('auction/<int:auction_id>/', views.auction_details_view, name='auction_details'),
]
# auctions/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Property(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    address = models.TextField()
    size = models.FloatField()
    property_type = models.CharField(max_length=100)  # e.g., "House", "Apartment"

    def __str__(self):
        return f"{self.property_type} at {self.address}"


class Auction(models.Model):
    STATUS_CHOICES = [
        ('ended', 'Ended'),
        ('coming', 'Coming Soon'),
        ('going_on', 'Going On'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='auctions')
    starting_bid = models.FloatField()
    reserve_price = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='coming')

    def __str__(self):
        return f"Auction for {self.property} by {self.seller.username}"

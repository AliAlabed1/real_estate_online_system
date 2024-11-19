

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    )
    usertype = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)


class Wallet(models.Model):
    buyer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet', limit_choices_to={'usertype': 'buyer'})
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Wallet of {self.buyer.username}"


class Bid(models.Model):
    auction = models.ForeignKey('auctions.Auction', on_delete=models.CASCADE, related_name='bids')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids', limit_choices_to={'usertype': 'buyer'})
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.buyer.username} on {self.auction}"
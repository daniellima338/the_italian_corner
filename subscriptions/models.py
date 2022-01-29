from django.contrib.auth.models import User
from django.db import models


class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class MonthlyWine(models.Model):
    name = models.CharField(max_length=254)
    description = models.TextField()
    region = models.CharField(max_length=254)
    image_url = models.URLField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

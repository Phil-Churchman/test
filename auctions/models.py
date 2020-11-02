from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    creation_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2)
    image_url = models.URLField(max_length=200, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    active = models.BooleanField()

    def __str__(self):
        return f"Listing by {self.user} of {self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid by {self.user} for {self.listing} of {self.bid_amount}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.TextField(max_length=256)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} regarding {self.listing}"

class Watch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} watching {self.listing}"

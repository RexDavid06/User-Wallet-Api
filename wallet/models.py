from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"
    
    


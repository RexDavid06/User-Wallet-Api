from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet - Balance: {self.balance}"
    
    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'


class WalletTransaction(models.Model):
    CREDIT = "credit"
    DEDIT = "debit"

    TRANSACTION_TYPE = [
        (CREDIT, 'Credit'),
        (DEDIT, 'Debit'),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference} - {self.amount}"
    
    class Meta:
        verbose_name = 'Wallet Transaction'
        verbose_name_plural = 'Wallet Transactions'
    

class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['key', 'user'], name='unique_idempotency_key_per_user')
        ]
        verbose_name = 'Idempotency Key'
        verbose_name_plural = 'Idempotency Keys'



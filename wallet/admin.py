from django.contrib import admin
from .models import Wallet, WalletTransaction, IdempotencyKey

# Register your models here.
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']

class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'created_at']

class IdempotencyKeyAdmin(admin.ModelAdmin):
    list_display = ['user', 'key']

admin.site.register(Wallet, WalletAdmin)
admin.site.register(WalletTransaction, WalletTransactionAdmin)
admin.site.register(IdempotencyKey, IdempotencyKeyAdmin)


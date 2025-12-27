from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Wallet, IdempotencyKey, WalletTransaction
from rest_framework.response import Response
from .serializers import AmountSerializer
from django.db import transaction, IntegrityError
from rest_framework import status   

# Create your views here.
class WalletBalanceView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        return Response({
            "wallet balance": wallet.balance 
        }, status=status.HTTP_200_OK)
    

class WalletCreditView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            return Response({
                "error": "Idempotency Key header is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']

        try:
            with transaction.atomic():
                #create idempotency key first
                IdempotencyKey.objects.create(
                    user=request.user,
                    key=idempotency_key
                )

                #lock wallet row
                wallet = Wallet.objects.select_for_update().get(user=request.user)
                #credit wallet
                wallet.balance += amount
                wallet.save()

                #log transaction
                WalletTransaction.objects.create(
                    wallet=wallet,
                    amount=amount,
                    transaction_type=WalletTransaction.CREDIT
                )
        except IntegrityError:
             return Response({
                 "error": "duplicate key"
             }, status=status.HTTP_409_CONFLICT)
        
        return Response({
            "message": "wallet has been credited",
            "wallet balance": wallet.balance
        }, status=status.HTTP_200_OK)

        
       
class WalletDebitView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        idempotency_key = request.headers.get("Idempotency-Key")
        if not idempotency_key:
            return Response({
                "error": "Idempotency Key header is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = AmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']

        try:
            with transaction.atomic():
                #create idempotency key for the logged in user
                IdempotencyKey.objects.create(
                    user=request.user,
                    key=idempotency_key
                )
                # lock the wallet row
                wallet = Wallet.objects.select_for_update().get(user=request.user)

                #check if wallet balance is less than amount to be debited
                if wallet.balance < amount:
                    return Response({
                        "error": "insufficient funds"
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                #if wallet balance is greater than amount, then the amount will be debited
                wallet.balance -= amount
                wallet.save()

                #log transactions
                WalletTransaction.objects.create(
                        wallet=wallet,
                        amount=amount,
                        transaction_type=WalletTransaction.DEDIT
                )

        except IntegrityError:
            return Response({
                "error": "duplicate key"
            }, status=status.HTTP_409_CONFLICT)
        return Response({
            "message": "wallet has been debited",
            "wallet balance": wallet.balance
        }, status=status.HTTP_200_OK)
    

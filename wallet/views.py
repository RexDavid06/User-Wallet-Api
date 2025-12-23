from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Wallet
from rest_framework.response import Response
from .serializers import AmountSerializer
from django.db import transaction
from rest_framework import status   

# Create your views here.
class WalletBalanceView(APIView):
    "retrieve user wallet balance"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        return Response({
            "wallet balance": wallet.balance
        })
    

class WalletCreditView(APIView):
    "credit user wallet balance"
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=request.user)
            wallet.balance += amount
            wallet.save()
            return Response({
                "message": "wallet credited",
                "balance": wallet.balance
            })


class WalletDebitView(APIView):
    "debit user wallet balance"
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AmountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        with transaction.atomic():
            wallet =Wallet.objects.select_for_update().get(user=request.user)
            if wallet.balance < amount:
                return Response({
                    "error": "insufficient funds"
                }, status=status.HTTP_400_BAD_REQUEST)
            wallet.balance -= amount
            wallet.save()
            return Response({
                "message": "wallet debited",
                "balance": wallet.balance
            })

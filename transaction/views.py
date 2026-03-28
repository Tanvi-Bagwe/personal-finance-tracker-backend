from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import ResponseFields, ResponseMessages
from .constant import TransactionFields
from .models import Transaction, Category
from .serializers import CreateTransactionSerializer, TransactionSerializer


class CreateTransactionView(APIView):
    """Create a new transaction"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateTransactionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # Check if category belongs to the user
        category_id = serializer.validated_data[TransactionFields.CATEGORY]
        try:
            category = Category.objects.get(id=category_id, user=request.user)
        except Category.DoesNotExist:
            raise ValidationError(ResponseMessages.INVALID_CATEGORY)

        transaction = Transaction.objects.create(
            user=request.user,
            category=category,
            amount=serializer.validated_data[TransactionFields.AMOUNT],
            type=serializer.validated_data[TransactionFields.TYPE],
            description=serializer.validated_data.get(TransactionFields.DESCRIPTION, ""),
            date=serializer.validated_data[TransactionFields.DATE]
        )

        return Response({
            ResponseFields.MESSAGE: ResponseMessages.TRANSACTION_RECORDED,
            TransactionFields.ID: transaction.id
        })


class ListTransactionsView(APIView):
    """Get all transactions for the user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class UpdateTransactionView(APIView):
    """Update transaction details"""
    permission_classes = [IsAuthenticated]

    def put(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        except Transaction.DoesNotExist:
            raise NotFound(ResponseMessages.TRANSACTION_NOT_FOUND)

        serializer = CreateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify category belongs to the user
        category_id = serializer.validated_data[TransactionFields.CATEGORY]
        try:
            category = Category.objects.get(id=category_id, user=request.user)
        except Category.DoesNotExist:
            raise ValidationError(ResponseMessages.INVALID_CATEGORY)

        transaction.amount = serializer.validated_data[TransactionFields.AMOUNT]
        transaction.category = category
        transaction.type = serializer.validated_data[TransactionFields.TYPE]
        transaction.description = serializer.validated_data.get(TransactionFields.DESCRIPTION, "")
        transaction.date = serializer.validated_data[TransactionFields.DATE]

        transaction.save()

        return Response({ResponseFields.MESSAGE: ResponseMessages.TRANSACTION_UPDATED})


class DeleteTransactionView(APIView):
    """Delete a transaction"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        except Transaction.DoesNotExist:
            raise NotFound(ResponseMessages.TRANSACTION_NOT_FOUND)

        transaction.delete()
        return Response({ResponseFields.MESSAGE: ResponseMessages.TRANSACTION_DELETED})


class RetrieveTransactionView(APIView):
    """Get a single transaction by ID"""
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id):
        # Filter by both transaction_id and user to prevent unauthorized access
        transaction = get_object_or_404(
            Transaction,
            id=transaction_id,
            user=request.user
        )

        serializer = TransactionSerializer(transaction)

        return Response(serializer.data)

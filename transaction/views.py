from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.constant import AuthFields
from .constant import TransactionFields
from .models import Transaction, Category
from .serializers import CreateTransactionSerializer, TransactionSerializer


class CreateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateTransactionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Ensure the category belongs to the user
        category_id = serializer.validated_data[TransactionFields.CATEGORY]
        try:
            category = Category.objects.get(id=category_id, user=request.user)
        except Category.DoesNotExist:
            return Response({ResponseFields.ERROR: "Invalid category selected"}, status=400)

        transaction = Transaction.objects.create(
            user=request.user,
            category=category,
            amount=serializer.validated_data[TransactionFields.AMOUNT],
            type=serializer.validated_data[TransactionFields.TYPE],
            description=serializer.validated_data.get(TransactionFields.DESCRIPTION, ""),
            date=serializer.validated_data[TransactionFields.DATE]
        )

        return Response({
            ResponseFields.MESSAGE: "Transaction recorded",
            TransactionFields.ID: transaction.id
        }, status=201)


class ListTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filtering by user and ordering by date descending
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class UpdateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        except Transaction.DoesNotExist:
            return Response({ResponseFields.ERROR: "Transaction not found"}, status=404)

        serializer = CreateTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        # Check category validity again if changing category
        category_id = serializer.validated_data[TransactionFields.CATEGORY]
        try:
            category = Category.objects.get(id=category_id, user=request.user)
        except Category.DoesNotExist:
            return Response({ResponseFields.ERROR: "Invalid category selected"}, status=400)

        transaction.amount = serializer.validated_data[TransactionFields.AMOUNT]
        transaction.category = category
        transaction.type = serializer.validated_data[TransactionFields.TYPE]
        transaction.description = serializer.validated_data.get(TransactionFields.DESCRIPTION, "")
        transaction.date = serializer.validated_data[TransactionFields.DATE]

        transaction.save()

        return Response({ResponseFields.MESSAGE: "Transaction updated"})


class DeleteTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        except Transaction.DoesNotExist:
            return Response({ResponseFields.ERROR: "Transaction not found"}, status=404)

        transaction.delete()
        return Response({ResponseFields.MESSAGE: "Transaction deleted"})


class RetrieveTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id):
        # SECURITY: Filter by both transaction_id AND the logged-in user
        # This prevents User A from seeing User B's transaction by ID
        transaction = get_object_or_404(
            Transaction,
            id=transaction_id,
            user=request.user
        )

        serializer = TransactionSerializer(transaction)

        return Response(serializer.data)

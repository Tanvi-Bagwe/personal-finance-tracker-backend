from django.urls import path

from .views import ListTransactionsView, CreateTransactionView, UpdateTransactionView, DeleteTransactionView, \
    RetrieveTransactionView

urlpatterns = [
    path("", ListTransactionsView.as_view()),
    path("create", CreateTransactionView.as_view()),
    path("<int:transaction_id>/update", UpdateTransactionView.as_view()),
    path("<int:transaction_id>/delete", DeleteTransactionView.as_view()),
    path("<int:transaction_id>", RetrieveTransactionView.as_view()),
]

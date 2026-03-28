from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth, Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.constants import ResponseMessages, ResponseFields
from dashboard.constant import DashboardFields
from reminder.models import Reminder
from datetime import date, timedelta

from transaction.models import Transaction


class DashboardSummaryView(APIView):
    """Get dashboard summary with income, expense and trends"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Fetch dashboard data for the authenticated user"""
        user = request.user

        # Calculate total income and expense (Coalesce handles None values)
        totals = Transaction.objects.filter(user=user).aggregate(
            total_income=Coalesce(Sum('amount', filter=Q(type='income')), 0),
            total_expense=Coalesce(Sum('amount', filter=Q(type='expense')), 0)
        )

        # Get expenses by category for pie chart
        category_data = Transaction.objects.filter(user=user, type='expense') \
            .values('category__name') \
            .annotate(value=Sum('amount')) \
            .order_by('-value')

        # Get last 6 months of transactions for trend graph
        six_months_ago = date.today() - timedelta(days=180)
        monthly_stats = Transaction.objects.filter(user=user, date__gte=six_months_ago) \
            .annotate(month=TruncMonth('date')) \
            .values('month', 'type') \
            .annotate(total=Sum('amount')) \
            .order_by('month')

        # Count pending and overdue reminders
        reminder_stats = {
            DashboardFields.PENDING: Reminder.objects.filter(user=user, is_completed=False).count(),
            DashboardFields.OVERDUE: Reminder.objects.filter(user=user, is_completed=False, due_date__lt=date.today()).count()
        }

        return Response({
            DashboardFields.SUMMARY: {
                DashboardFields.INCOME: totals['total_income'],
                DashboardFields.EXPENSE: totals['total_expense'],
                DashboardFields.BALANCE: totals['total_income'] - totals['total_expense']
            },
            "category_distribution": category_data,
            "trends": monthly_stats,
            "reminders": reminder_stats,
            ResponseFields.MESSAGE: ResponseMessages.DASHBOARD_SUCCESSFUL
        })
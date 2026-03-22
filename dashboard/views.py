from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from dashboard.constant import DashboardFields
from reminder.models import Reminder
from datetime import date, timedelta

from transaction.models import Transaction


class DashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1. Calculate Stat Card Totals
        totals = Transaction.objects.filter(user=user).aggregate(
            total_income=Sum('amount', filter=Q(type='income')) or 0,
            total_expense=Sum('amount', filter=Q(type='expense')) or 0
        )

        # 2. Expense by Category (Pie Chart)
        category_data = Transaction.objects.filter(user=user, type='expense') \
            .values('category__name') \
            .annotate(value=Sum('amount')) \
            .order_by('-value')

        # 3. Monthly Trend (Last 6 Months)
        six_months_ago = date.today() - timedelta(days=180)
        monthly_stats = Transaction.objects.filter(user=user, date__gte=six_months_ago) \
            .annotate(month=TruncMonth('date')) \
            .values('month', 'type') \
            .annotate(total=Sum('amount')) \
            .order_by('month')

        # 4. Reminder Pulse
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
            "reminders": reminder_stats
        })
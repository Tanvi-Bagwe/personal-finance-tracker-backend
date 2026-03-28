from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from accounts.constant import AuthFields
from core.constants import ResponseFields, ResponseMessages
from .models import Reminder
from .serializers import ReminderSerializer, CreateReminderSerializer
from .constant import ReminderFields

# 1. LIST ALL REMINDERS
class ReminderListView(APIView):
    """Get all pending reminders for the user"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reminders = Reminder.objects.filter(
            user=request.user,
            is_completed=False
        ).order_by('due_date')
        serializer = ReminderSerializer(reminders, many=True)
        return Response(serializer.data)

# 2. CREATE REMINDER
class ReminderCreateView(APIView):
    """Create a new reminder"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateReminderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reminder = Reminder.objects.create(
            user=request.user,
            title=serializer.validated_data[ReminderFields.TITLE],
            amount=serializer.validated_data.get(ReminderFields.AMOUNT),
            due_date=serializer.validated_data[ReminderFields.DUE_DATE],
            reminder_days_before=serializer.validated_data.get(ReminderFields.REMINDER_DAYS, 1)
        )
        return Response({ResponseFields.MESSAGE: ResponseMessages.REMINDER_CREATED, "id": reminder.id})

# 3. UPDATE REMINDER (Full Edit)
class ReminderUpdateView(APIView):
    """Update reminder details"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        reminder = get_object_or_404(Reminder, id=pk, user=request.user)
        serializer = CreateReminderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        reminder.title = serializer.validated_data[ReminderFields.TITLE]
        reminder.amount = serializer.validated_data.get(ReminderFields.AMOUNT)
        reminder.due_date = serializer.validated_data[ReminderFields.DUE_DATE]
        reminder.reminder_days_before = serializer.validated_data.get(ReminderFields.REMINDER_DAYS, 1)
        reminder.save()

        return Response({ResponseFields.MESSAGE: ResponseMessages.REMINDER_UPDATED})

# 4. DELETE REMINDER
class ReminderDeleteView(APIView):
    """Delete a reminder"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        reminder = get_object_or_404(Reminder, id=pk, user=request.user)
        reminder.delete()
        return Response({ResponseFields.MESSAGE: ResponseMessages.REMINDER_DELETED})

# 5. REMINDER ACTION (Patch for Status Toggle)
class ReminderActionView(APIView):
    """Update reminder status (mark as read/completed)"""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        reminder = get_object_or_404(Reminder, id=pk, user=request.user)

        if 'is_read' in request.data:
            reminder.is_read = request.data['is_read']
        if 'is_completed' in request.data:
            reminder.is_completed = request.data['is_completed']

        reminder.save()
        return Response({ResponseFields.MESSAGE: ResponseMessages.REMINDER_UPDATED})
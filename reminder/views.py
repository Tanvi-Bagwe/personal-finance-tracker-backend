from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from accounts.constant import AuthFields
from .models import Reminder
from .serializers import ReminderSerializer, CreateReminderSerializer
from .constant import ReminderFields

# 1. LIST ALL REMINDERS
class ReminderListView(APIView):
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateReminderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        reminder = Reminder.objects.create(
            user=request.user,
            title=serializer.validated_data[ReminderFields.TITLE],
            amount=serializer.validated_data.get(ReminderFields.AMOUNT),
            due_date=serializer.validated_data[ReminderFields.DUE_DATE],
            reminder_days_before=serializer.validated_data.get(ReminderFields.REMINDER_DAYS, 1)
        )
        return Response({ResponseFields.MESSAGE: "Reminder created successfully", "id": reminder.id}, status=201)

# 3. UPDATE REMINDER (Full Edit)
class ReminderUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        reminder = get_object_or_404(Reminder, id=pk, user=request.user)
        serializer = CreateReminderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        reminder.title = serializer.validated_data[ReminderFields.TITLE]
        reminder.amount = serializer.validated_data.get(ReminderFields.AMOUNT)
        reminder.due_date = serializer.validated_data[ReminderFields.DUE_DATE]
        reminder.reminder_days_before = serializer.validated_data.get(ReminderFields.REMINDER_DAYS, 1)
        reminder.save()

        return Response({ResponseFields.MESSAGE: "Reminder updated successfully"})

# 4. DELETE REMINDER
class ReminderDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        reminder = get_object_or_404(Reminder, id=pk, user=request.user)
        reminder.delete()
        return Response({ResponseFields.MESSAGE: "Reminder deleted successfully"})

# 5. REMINDER ACTION (Patch for Status Toggle)
class ReminderActionView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        reminder = get_object_or_404(Reminder, id=pk, user=request.user)

        if 'is_read' in request.data:
            reminder.is_read = request.data['is_read']
        if 'is_completed' in request.data:
            reminder.is_completed = request.data['is_completed']

        reminder.save()
        return Response({ResponseFields.MESSAGE: "Reminder status updated"})
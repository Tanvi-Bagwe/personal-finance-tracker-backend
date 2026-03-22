from django.urls import path
from .views import ReminderListView, ReminderActionView, ReminderCreateView, ReminderUpdateView, \
    ReminderDeleteView

urlpatterns = [
    path("", ReminderListView.as_view()),  # GET (List)
    path("create", ReminderCreateView.as_view()),  # POST (Create)
    path("<int:pk>/update", ReminderUpdateView.as_view()),  # PUT (Edit)
    path("<int:pk>/delete", ReminderDeleteView.as_view()),  # DELETE (Remove)
    path("<int:pk>/action", ReminderActionView.as_view()),  # PATCH (Read/Complete)
]

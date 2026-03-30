from django.urls import path, include
from . import views
from .views import displayEvents

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    # ------- START PAGE -----#
    path('', views.start_page, name='start_page'),


    # -------- CALENDAR -------#

    path('calendar/', views.calendar, name='calendar'),
    path('viewMore/<int:year>/<int:month>/<int:day>/', views.viewMore, name='viewMore'),

    # -------- PERSONAL JOURNAL -------#
    path('journal/', views.journal, name='journal'),
    path('viewJournalEntries/', views.viewJournalEntries, name='viewJournalEntries'),
    path('add_entry/', views.add_entry, name='add_entry'),

    # ------- REGISTER PAGE -------#
    path('register/', views.register, name='register'),

    # -------- lOG IN ---------#
    path('login/', views.log_in, name='log_in'),

    # --------- LOG OUT ------#
    path('user_logout', views.user_logout, name='user_logout'),


    # --------- FutureLogs; goals: ------#
    path('create_goal', views.create_goal, name='create_goal'),
    path('toggle/<int:goal_id>/', views.Toggle_goals, name='Toggle_goals'),
    path('update_goal/<str:pk>/', views.update_goal, name='update_goal'),
    # delete goal from database
    path('delete_goal/<str:pk>', views.delete_goal, name='delete_goal'),

    # --------- Future Logs ------#
    path('FutureLogsGoals/', views.FutureLogsGoals, name='FutureLogsGoals'),
    path('create_logs/', views.create_logs, name='create_logs'),
    # delete list and all of its tasks from database
    path('delete_log/<str:pk>', views.delete_log, name='delete_log'),

    path('update_log_name/<str:pk>', views.update_log_name, name='update_log_name'),

    # ------------ Events ------------#
    path('add_Event/', views.addEvent, name="add_event"),
    path('viewEvent/<str:pk>', views.viewEvent, name="viewEvent"),
    path('updateEvent/<str:pk>', views.updateEvent, name='updateEvent'),
    path('toggle_event/<int:event_id>/', views.toggle_event, name="toggle_event"),
    #delete event from database
    path('deleteEvent/<str:pk>', views.deleteEvent, name='deleteEvent'),

    # --------- WEEKLY SCHEDULE --------#
    # path('weekly_schedule/<int:more_>', views.weekly_schedule, name='weekly_schedule'),
    path('back_to_weekly/', views.back_to_weekly, name='back_to_weekly'),
    path('weekly_schedule/', views.weekly_schedule, name='weekly_schedule'),
    path('next_/<str:day>', views.next_, name='next_'),
    path('prev/<str:day>', views.prev, name='prev'),

#------------ Events displaying in different ways --------------------------
    path('displayEvents/', views.displayEvents, name="display_events"),

    path('events_of_the_day/', views.events_of_the_day, name='events_of_the_day'),

    #----- NOTIFICATION ----#
    path('mark_notification_read/<int:notif_id>/', views.mark_notification_read,
         name='mark_notification_read'),
path('mark_all_notifications_read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

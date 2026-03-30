from typing import Protocol

# from aiohttp import request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import auth
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from .models import Event, Logs, Goal, JournalEntry, Notification
from .forms import CreateUserForm, LoginForm, CreateGoalForm, CreateLogsForm, EventForm, EntryForm
from django.urls import reverse

from calendar import HTMLCalendar, weekday
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from django.utils.html import escapejs
from django.core.paginator import Paginator

import re#is needed for weekly events next and prev functions to work

# global variables for next and prev buttons in weekly schedule

# For activation #

#from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


def start_page(request):
    return render(request, 'start_page.html')


#Displays event in json format for the calendar
def displayEvents(request):
    events = Event.objects.filter(user_id=request.user.id)
    return JsonResponse({"events": list(events.values())})


@login_required
def calendar(request):
    create_notifications(request.user)
    events = Event.objects.filter(user_id=request.user.id)
    event_form = EventForm(request.POST)
    return render(request,
                  'calendar.html',
                  {'events': events, 'event_form': event_form,})


def journal(request):
    entry_form = EntryForm(request.POST)
    return render(request, 'journal.html', {"entry_form": entry_form})

def viewJournalEntries(request):
    # Retrieve all journal entries from the database that belong to logged-in user
    journals = JournalEntry.objects.filter(user_id=request.user.id)

    # Create a Paginator with 2 entries per page
    paginator = Paginator(journals, 2)  # Show 2 entries per page

    # Get the current page number from the GET parameters (defaults to 1 if not provided)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)  # Get the Page object for the current page

    # Pass the Page object (page_obj) to the template for iteration
    return render(request, 'journal.html', {'page_obj': page_obj})

def add_entry(request):
    if request.method == 'POST':
        entry_form = EntryForm(request.POST)
        if entry_form.is_valid():
            journal_entry = entry_form.save(commit=False) #don't save the form yet
            journal_entry.date_of_entry = datetime.today().date() #get the current date from user's device
            journal_entry.user = request.user
            journal_entry.save()
            return redirect('journal')
        else:
            return HttpResponse("something went wrong with the event form")
    else:
        entry_form = EntryForm()
        return render(request, 'journal.html', {'entry_form': entry_form})


def addEvent(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        event_form.instance.user = request.user

        if event_form.is_valid():
            #get the date_of_event from the POST data of the form
            date_of_event = request.POST.get('date_of_event')
            #set the date retrieved date_of_event to the form
            event_instance = event_form.save(commit=False)
            event_instance.date_of_event = date_of_event

            event_instance.user = request.user

            event_instance.save()
            return redirect('calendar')
        else:
            return HttpResponse("something went wrong with the event form")
    else:
        event_form = EventForm()  #for GET request, show the form
        return render(request, 'calendar.html', {'event_form': event_form})


# ----- for register page -------#
def register(request):
    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('calendar')

    return render(request, "register.html", {'form': form})

#     return render(request, "register.html", {'form': form})

# -------- log in ------#

def log_in(request):
    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect('calendar')

                # return HttpResponse('Logged in as %s' % user.username)

    context = {'form': form}

    return render(request, 'log_in.html', context=context)


# ------- LOG OUT -----#

def user_logout(request):
    auth.logout(request)

    return redirect('start_page')

# -------- Future logs and goals ------------#
# ----Goals-----
def create_goal(request):
    form = CreateGoalForm()
    if request.method == 'POST':
        form = CreateGoalForm(request.POST, request.FILES)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('FutureLogsGoals')

    context = {'form': form}
    return render(request, 'FutureLogs&Goals.html', context=context)

# Update tasks

def update_goal(request, pk):
    goals = Goal.objects.get(id=pk)
    # all_goals = Goal.objects.get(id=pk)
    UpdateGoalsform = CreateGoalForm(instance=goals)
    if request.method == 'POST':
        UpdateGoalsform = CreateGoalForm(request.POST, instance=goals)
        if UpdateGoalsform.is_valid():
            UpdateGoalsform.save()
            return redirect('FutureLogsGoals')
    context = {'UpdateGoalsform': UpdateGoalsform}
    return render(request, 'updateGoals.html', context=context)



#delete Goals
def delete_goal(request, pk):
    goal = Goal.objects.get(id=pk)
    goal.delete()
    return redirect('FutureLogsGoals')


# ------- Logs --------
def create_logs(request):
    form_ = CreateLogsForm()
    if request.method == 'POST':
        form_ = CreateLogsForm(request.POST, request.FILES)
        if form_.is_valid():
            log = form_.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('FutureLogsGoals')

    context = {'form_': form_}
    return render(request, 'FutureLogs&Goals.html', context=context)

@login_required
def update_log_name(request, pk):
    log = Logs.objects.get(id=pk)
    UpdateLogsForm = CreateLogsForm(instance=log)
    if request.method == 'POST':
        UpdateLogsForm = CreateLogsForm(request.POST, instance=log)
        if UpdateLogsForm.is_valid():
            UpdateLogsForm.save()
            return redirect('FutureLogsGoals')
    context = {'UpdateLogsForm': UpdateLogsForm}
    return render(request, 'updateLogs.html', context=context)


#Delete list
@login_required
def delete_log(request, pk):
    log = Logs.objects.get(id=pk)
    log.delete()
    return redirect('FutureLogsGoals')


def FutureLogsGoals(request):
    log = Logs.objects.filter(user_id=request.user.id)
    goals = Goal.objects.filter(user_id=request.user.id)

    logForm = CreateLogsForm()
    goalForm = CreateGoalForm()

    context = {'goals': goals, 'log': log, 'logForm': logForm, 'goalForm': goalForm}
    return render(request, 'FutureLogs&Goals.html', context=context)

def Toggle_goals(request, goal_id):
    goals = Goal.objects.get(pk=goal_id)
    goals.completed = not goals.completed
    goals.save()
    return redirect('FutureLogsGoals')

# -------------------  Events -------------------------
# Add an event
@login_required
def addEvent(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST)
        event_form.instance.user = request.user
        if event_form.is_valid():
            # get the date_of_event from the POST data of the form
            date_of_event = request.POST.get('date_of_event')

            # set the date retrieved date_of_event to the form
            event_instance = event_form.save(commit=False)
            event_instance.user = request.user
            event_instance.date_of_event = date_of_event

            event_instance.save()
            return redirect('calendar')
        else:
            return HttpResponse("something went wrong with the event form")
    else:
        event_form = EventForm()  # for GET request, show the form
        return render(request, 'calendar.html', {'event_form': event_form})

#View event
@login_required
def viewEvent(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}
    return render(request, 'weekly_schedule.html',context=context)

def viewMore(request, year, month, day):

    print("viewMore function was run")

    dateCalendar = datetime(year, month, day) #calendar date that is passed to the function
    dateWeekly = datetime.today() #first date of the weekly
    global increase, decrease

    diff = abs(dateCalendar.day - dateWeekly.day) #difference between days (only positive)

    if(dateCalendar.day > dateWeekly.day):
        increase =  diff
        next_(request)
        return redirect('next_')


    elif(dateCalendar.day < dateWeekly.day):
        decrease = diff
        prev(request)
        return redirect('prev')

    context ={'next_': next_, 'prev': prev, 'increase': increase, 'decrease': decrease}

    return render(request, 'weekly_schedule.html', context=context)


def toggle_event(request, event_id):
    events = Event.objects.get(pk=event_id)
    events.is_completed = not events.is_completed
    events.save()
    return redirect('weekly_schedule')


# Update event
@login_required
def updateEvent(request, pk):
    all_events = Event.objects.filter(user_id=request.user.id)
    event = Event.objects.get(id=pk)
    event_form = EventForm(instance=event)

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            return redirect('weekly_schedule')

    # Display events on edit page
    weekDay = datetime.today()  # gets today's date
    weekDay2 = weekDay + timedelta(days=1)  # gets the day after
    weekDay3 = weekDay + timedelta(days=2)  # gets the 3rd day after the first one
    # Filters to only get events that are associated with the same days
    display_events = events_of_the_day(request, weekDay, weekDay2, weekDay3)

    context = {'weekDay': weekDay, 'weekDay2': weekDay2, 'weekDay3': weekDay3
        , 'event_form': event_form, 'all_events': all_events}

    # context = {'event': event, 'all_events': all_events, 'event_form': event_form, 'test': test}
    return render(request, 'updateEvents.html', context=context)


def back_to_weekly(request):
    return redirect('weekly_schedule')


@login_required
def deleteEvent(request, pk):
    event = Event.objects.get(id=pk)
    event.delete()
    return redirect('weekly_schedule')


# ----------------- weekly_schedule ------------------------
#Displays events
def events_of_the_day( request, day1, day2, day3):
    # Filters to only get events that are associated with the same days
    day1_events = Event.objects.filter(date_of_event__day=day1.day, date_of_event__month=day1.month, user_id=request.user.id)
    day2_events = Event.objects.filter(date_of_event__day=day2.day, date_of_event__month=day2.month, user_id=request.user.id)
    day3_events = Event.objects.filter(date_of_event__day=day3.day, date_of_event__month=day3.month, user_id=request.user.id)

    context = {'day1_events':day1_events, 'day2_events':day2_events, 'day3_events':day3_events}
    return context

@login_required
def weekly_schedule(request):
    event_form = EventForm(request.POST)
    all_events = Event.objects.filter(user_id=request.user.id)
    start_date = request.GET.get('date')

    if start_date:
        weekDay = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        weekDay = datetime.today()  # gets today's date

    weekDay2 = weekDay + timedelta(days=1)  # gets the day after
    weekDay3 = weekDay + timedelta(days=2)  # gets the 3rd day after the first one


    display_events = events_of_the_day(request, weekDay, weekDay2, weekDay3)
    context = {'weekDay': weekDay, 'weekDay2': weekDay2, 'weekDay3': weekDay3
        , 'event_form': event_form, 'all_events': all_events, 'display_events': display_events}
    return render(request, 'weekly_schedule.html', context=context)


# --------- Goes to next few days ------------------
@login_required
def next_(request, day):
    # Search the string
    match_str = re.search(r'\d{4}-\d{2}-\d{2}', day)
    #Format date
    result = datetime.strptime(match_str.group(), '%Y-%m-%d').date()
    # go to next day
    nextDay = result + timedelta(days=1)

    return redirect(reverse('weekly_schedule') + '?date={}'.format(nextDay))


# Goes to previous days
@login_required
def prev(request, day):
    # Search the string
    match_str = re.search(r'\d{4}-\d{2}-\d{2}', day)
    # Format date
    result = datetime.strptime(match_str.group(), '%Y-%m-%d').date()
    # go to next day
    prevDay = result - timedelta(days=1)

    return redirect(reverse('weekly_schedule') + '?date={}'.format(prevDay))


#----NOTIFICATION FEATURE ----#
def create_notifications(user):
    today = datetime.today()
    upcoming_event = Event.objects.filter(
        user =user,
        date_of_event__gt=today,
        date_of_event__lte=today + timedelta(days=2)
    )
    print("Upcoming events found:", upcoming_event)

    for event in upcoming_event:

        message = f"Upcoming event: {event.event_name} on {event.date_of_event}"

        print("Checking event for notifications:", message)

        if not Notification.objects.filter(user=user, message=message).exists():
            print("Checking event for notifications:", message)
            Notification.objects.create(user=user, message=message)

            #filter(user=user, message__icontains=event.event_name, is_read=False).exists()):
            #message = f"Upcoming event: {event.event_name} on {event.date_of_event}"
            #Notification.objects.create(user=user, message=message)
            #message = f"Upcoming event: {event.event_name} on {event.date_of_event}").exists():
            #Notification.objects.create(user=user, message=message)


@login_required
def mark_notification_read(request, notif_id):
    notification = Notification.objects.get(id=notif_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect(request.META.get('HTTP_REFERER', 'calendar'))

@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect(request.META.get('HTTP_REFERER', 'calendar'))

#Password for an email
#SCHOOL123
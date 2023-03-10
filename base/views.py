from django.shortcuts import render, redirect
from .models import User, Event, Submission
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def login_page(request):
    page = 'login'

    if request.method == 'POST':
        user = authenticate(
            email=request.POST['email'],
            password= request.POST['password']
            )
        if user is not None:
            login(request, user)
            return redirect('home')

    context = {'page': page}
    return render(request, 'login_register.html', context)


def register_page(request):
    page = 'register'
    form = CustomCreation()


    if request.method == 'POST':
        form = CustomCreation(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')

def index(request):
    users= User.objects.filter(event_participant=True)
    events = Event.objects.all()
    context = {'users': users, 'events': events}
    return render(request, "home.html", context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, "profile.html", context)


@login_required(login_url='/login')
def account_page(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account.html')


def event_page(request, pk):
    event = Event.objects.get(id=pk)
    registered = False
    submitted = False
    if request.user.is_authenticated:

        registered = request.user.events.filter(id= event.id).exists()
        submitted = Submission.objects.filter(event=event, participant=request.user).exists()
    context = {'event': event, 'registered': registered, 'submitted': submitted}
    return render(request, 'event.html', context)



@login_required(login_url='/login')
def register_confirmation(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}
    if request.method == 'POST':
        event.participant.add(request.user) 
        return redirect('event', pk=event.id)
    return render(request, 'confirmation.html', context)


@login_required(login_url='/login')
def project_sub(request, pk):
    event= Event.objects.get(id=pk)
    form = SubmissionForm()
    if request.method == 'POST':
        form = SubmissionForm(request.POST) # This prefills the logged in user's details ,initial={'event': event, 'participant':request.user}
        if form.is_valid:
            submission = form.save(commit=False)
            submission.participant =request.user
            submission.event = event
            submission.save() # This saves it to the database
            return redirect('my-account')
    context ={'event': event, 'form': form}
    return render(request, 'submit.html', context)

@login_required(login_url='/login')
def update_sub(request, pk):
    submission = Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse('You Are not Authorized To Update This Submission')
    event = submission.event
    form = SubmissionForm(instance=submission)

    if request.method == 'POST':
        form = SubmissionForm(request.POST,instance=submission)
        if form.is_valid:
            form.save()
            return redirect('my-account')
    context ={'event': event, 'form': form}
    return render(request, 'submit.html', context)
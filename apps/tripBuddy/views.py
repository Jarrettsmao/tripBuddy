from django.shortcuts import render, redirect, reverse
from . models import User, Trip
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'tripBuddy/index.html')

def dashboard(request):
    if 'userID' not in request.session:
        return redirect(index)
    else:
        user = User.objects.get(id = request.session['userID'])
        context={
            'your_trips': Trip.objects.filter(creator=user),
            'joined_trips': Trip.objects.filter(vacationer=user),
            'other_trips': Trip.objects.exclude(vacationer=user).exclude(creator=user),
            'username': request.session['username'],
            'userID': request.session['userID'],
        }
        return render(request, 'tripBuddy/dashboard.html', context)

def register(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(index)

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pw = bcrypt.hashpw(request.POST['rPass'].encode(), bcrypt.gensalt())
        request.session['username'] = fname
        User.objects.create(first_name = fname, last_name = lname, email = email, password = pw)
        user = User.objects.get(email = email)
        request.session['userID'] = user.id
    return redirect(dashboard)

def login(request):
    if request.method == "POST":
        print(User.objects.filter(email = request.POST['lemail']).count())
        if User.objects.filter(email = request.POST['lemail']).count() == 0:
            messages.error(request, "User does not exist.")
            return redirect(index)
        elif User.objects.filter(email = request.POST['lemail']).count() == 1:
            lemail = User.objects.get(email=request.POST['lemail'])
            if bcrypt.checkpw(request.POST['lpass'].encode(), lemail.password.encode()):
                request.session['username'] = lemail.first_name
                request.session['userID'] = lemail.id
                return redirect(dashboard)
            else:
                messages.error(request, "Password is incorrect.")
                return redirect(index)

def logout(request):
    request.session.clear()
    return redirect(index)

def new(request):
    context={
        'username': request.session['username'],
        'userID': request.session['userID'],
    }
    return render(request, 'tripBuddy/newTrip.html', context)

def newTrip(request):
    errors = User.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(new)
    elif request.method == "POST":
        dest = request.POST['dest']
        sDate = request.POST['sDate']
        eDate = request.POST['eDate']
        plan = request.POST['plan']
        user = User.objects.get(id = request.session['userID'])
        Trip.objects.create(destination = dest, start_date = sDate, end_date = eDate, plan = plan, creator=user)
        return redirect(dashboard)

def remove_trip(request, trip_id):
    trip_to_delete = Trip.objects.get(id = trip_id)
    trip_to_delete.delete()
    return redirect(dashboard)

def show_trip(request, trip_id):
    if 'userID' not in request.session:
        return redirect(index)
    trip = Trip.objects.get(id = trip_id)
    joined = trip.vacationer.all()
    request.session['trip_id'] = trip_id

    context={
        "username": request.session['username'],
        'userID': request.session['userID'],
        "trip_info": trip,
        'joined': joined,
    }
    return render(request, "tripBuddy/show.html", context)

def edit_trip(request, trip_id):
    if 'userID' not in request.session:
        return redirect(index)
    trip = Trip.objects.get(id = trip_id)
    context ={
        "username": request.session['username'],
        'userID': request.session['userID'],
        "trip_id": request.session['trip_id'],
        "trip_info": trip,
    }
    return render(request, "tripBuddy/editTrip.html", context)

def edit(request, trip_id):
    errors = User.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(reverse("edit_trip", kwargs={"trip_id": trip_id}))
    elif request.method == "POST":
        trip_to_edit = Trip.objects.get(id=trip_id)
        trip_to_edit.destination = request.POST['dest']
        trip_to_edit.plan = request.POST['plan']
        trip_to_edit.start_date = request.POST['sDate']
        trip_to_edit.end_date = request.POST['eDate']
        trip_to_edit.save() 
        return redirect(dashboard)

def add_trip(request, trip_id):
    trip = Trip.objects.get(id = trip_id)
    user = User.objects.get(id = request.session['userID'])
    trip.vacationer.add(user)
    return redirect(dashboard)

def giveup_trip(request, trip_id):
    trip = Trip.objects.get(id = trip_id)
    user = User.objects.get(id = request.session['userID'])
    trip.vacationer.remove(user)
    return redirect(dashboard)
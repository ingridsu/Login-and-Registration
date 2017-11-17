from django.shortcuts import render, HttpResponse, redirect
from models import *
from django.contrib import messages
import datetime


# Create your views here.

def index(request):
    # Giving value to session
    try: request.session['user']

    except KeyError:
        request.session['user'] = []

    if request.session['user']:
        return redirect('/success')
    
    return render(request,'index.html')


def success(request):

    return render(request,'success.html')

def add(request):
    errors = User.objects.basica_validator(request.POST)
    hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    if len(errors):
        for tag, error in errors.items():
            messages.error(request,error, extra_tags=tag)
        return redirect('/')
    
    User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'],email=request.POST['email'], password = hashpw, age = request.POST['date'], birthday = request.POST['date'], gender = request.POST['gender'], created_at = datetime.datetime.now)
    
    user = User.objects.filter(email = request.POST['email'])[0]
    request.session['user'] = user.id 
    request.session['name'] = user.first_name
    #Becasue we got a queryset therefore we need to assign each one

    return redirect('/success')


def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for tag, error in errors.items():
            messages.error(request,error, extra_tags=tag)
        return redirect('/')
    
    userinfo = User.objects.filter(email = request.POST['email'])[0]

    if userinfo:
        if not bcrypt.hashpw(request.POST['password'].encode(), userinfo.password.encode()):
            messages.error(request,"Invalid password")
            return redirect('/')
        else:
            request.session['user'] = userinfo.id
            request.session['name'] = userinfo.first_name
            return redirect('/success')   

    else:
        messages.error(request,"Invalid Email")
        return redirect('/')

def logout(request):
    request.session.pop('user',None)

    return redirect('/')
    
    
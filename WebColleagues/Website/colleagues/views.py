from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import warning, error, success
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse
from pathlib import Path


# Create your views here.

def home(request):
    data = {'title': 'Homepage'}
    if request.user.is_staff: data['users'] = User.objects.all()
    return render(request, 'home.html', data)

def signup(request):
    data = {'title': 'Register'}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        data['username'] = username
        data['password'] = password
        data['first_name'] = first_name
        data['last_name'] = last_name
        data['email'] = email
        data['phone'] = phone
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.profile.phone = phone
            login(request, user)
            success(request, 'You have successfully registered')
            return redirect('home')
        except IntegrityError: error(request, 'Username is not unique')
    return render(request, 'signup.html', data)

def login_(request):
    data = {'title': 'Login'}
    if request.method != 'POST': return render(request, 'login.html', data)
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user is None:
        data['username'] = request.POST.get('username')
        error(request, 'Incorrect credentials')
        return render(request, 'login.html', data)
    else:
        login(request, user)
        return redirect('home')

def logout_(request):
    logout(request)
    return redirect('home')

def my_account(request):
    if not request.user.is_authenticated:
        warning(request, 'You are not authorized. Please login first.')
        return redirect('home')
    data = {'title': 'My Account'}
    return render(request, 'profile.html', data)

def set_benefits(request, pk):
    if not request.user.is_staff:
        warning(request, 'You have no permission.')
        return redirect('home')
    data = {'title': 'Set benefits', 'user_': User.objects.get(pk=pk)}
    return render(request, 'set_benefits.html', data)

def save_benefits(request, pk):
    if request.method != 'POST': return redirect('set_benefits')
    if not request.user.is_staff: warning(request, 'You have no permission.')
    else:
        user = User.objects.get(pk=pk)
        user.profile.position = request.POST.get('position')
        user.profile.salary = request.POST.get('salary')
        user.profile.unused_vacation_days = request.POST.get('unused_vacation_days')
        user.save()
    return redirect('home')

def upload_img(request):
    if request.method != 'POST': return redirect('profile')
    if not request.user.is_authenticated:
        warning(request, 'You are not authorized. Please login first.')
        return redirect('home')
    user_id = request.user.pk
    user = User.objects.get(pk=user_id)
    image = request.FILES['myfile']
    user.profile.photo = request.FILES['myfile']
    user.save()
    return redirect('profile')

def media_ret(request, media_url):
    with open(settings.MEDIA_ROOT / media_url, 'rb') as file:
        return HttpResponse(file.read(), content_type=EXT_TO_TYPE.get(Path(media_url).suffix))

def static_ret(request, static_url):
    with open(settings.STATIC_ROOT / static_url, 'rb') as file:
        return HttpResponse(file.read(), content_type=EXT_TO_TYPE.get(Path(static_url).suffix))

EXT_TO_TYPE = {'.css': 'text/css',
               '.png': 'image/png',
               '.js': 'text/javascript',
               '.svg': 'image/svg+xml',
               '.jpg': 'image/jpeg',
               '.jpeg': 'image/jpeg',
               '.ico':'image/vnd.microsoft.icon',
               '.gif': 'image/gif',
               '.bmp': 'image/bmp',
               '.webp': 'image/webp',
               '.tif': 'image/tiff',
               '.tiff': 'image/tiff'
}

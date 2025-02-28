from django.shortcuts import render, redirect , HttpResponse
from .forms import Hod_Registration
from django.db import IntegrityError 
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# this fucntion will add new item and show all items 
# def add_show(request):
#     if request.method == 'POST':
#         print(request.POST)
#         fm = Hod_Registration(request.POST)
#         if fm.is_valid():
#             nm = fm.cleaned_data['name']
#             em = fm.cleaned_data['email']
#             pw = fm.cleaned_data['password']

#             reg = User(name=nm, email=em, password=pw)
#             reg.save()
#             return redirect('/')  
#     else:
#         fm = Hod_Registration()
#     hods = User.objects.all()
#     return render(request, 'add_user/addandshow.html', {'form': fm, 'hod': hods})

def add_show(request):
    if request.method == 'POST':
        print("Request POST Data:", request.POST)  # Debugging

        fm = Hod_Registration(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']

            # Prevent empty or whitespace-only names
            if not nm.strip():
                messages.error(request, "Name cannot be empty!")
            elif User.objects.filter(name=nm).exists():
                messages.error(request, "User with this name already exists!")
            elif User.objects.filter(email=em).exists():
                messages.error(request, "User with this email already exists!")
            else:
                try:
                    # Ensure user can log in
                    reg = User(name=nm, email=em, username=em,  is_staff=True)  #  have access to Django Admin
                    reg.set_password(pw) 
                    reg.save()
                    messages.success(request, "User added successfully!")
                    return redirect('/addandshow/')  
                except IntegrityError:
                    messages.error(request, "Error: Duplicate entry detected.")
                except Exception as e:
                    messages.error(request, f"Unexpected error: {e}")

    else:
        fm = Hod_Registration()

    hods = User.objects.all()
    return render(request, 'add_user/addandshow.html', {'form': fm, 'hod': hods})


def update_data(request, id):
    pi = get_object_or_404(User, pk=id)  
    
    if request.method == 'POST':
        fm = Hod_Registration(request.POST, instance=pi)  
        if fm.is_valid():
            fm.save()
            return redirect('/')  
    else:
        fm = Hod_Registration(instance=pi)  
    
    return render(request, 'add_user/updateuser.html', {'form': fm})  


# This function will delete data

def delete_data(request, id):
        pi = get_object_or_404(User, pk=id)

        if request.method == 'POST':
            pi.delete()
            return redirect('/')
    
        return render(request, "add_user/confirm_delete.html", {'user': pi})

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        # user = User.objects.all()
        # print(user[3].username)
        # return HttpResponse(user)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page if login is successful
        else:
            messages.error(request, "Username or password is incorrect!")

    return render(request, 'add_user/login.html')  # Correct template path

#  Logout View
@login_required
def LogoutPage(request):
    logout(request)
    return redirect('/')  # Redirect to login page after logout

# Home Page (Protected)
@login_required
def Home(request):
    return render(request, 'home.html')  # Load home.html

def dashboard(request):
    return render(request, 'add_user/home.html')  # Loads the dashboard page

def users(request):
    return render(request, 'users.html')  # Loads the users page

def settings(request):
    return render(request, 'settings.html')  # Loads the settings page
 


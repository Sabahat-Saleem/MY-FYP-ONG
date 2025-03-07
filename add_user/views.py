from django.shortcuts import render, redirect , HttpResponse
from .forms import Travel_Registration
from .forms import UserUpdateForm
from django.db import IntegrityError 
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import logout

def add_show(request):
    if request.method == 'POST':
        print("Request POST Data:", request.POST)  # Debugging

        fm = Travel_Registration(request.POST)
        if fm.is_valid():
            fn = fm.cleaned_data['first_name']
            ln = fm.cleaned_data['last_name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']

            full_name = f"{fn} {ln}".strip()

            if not fn.strip() or not ln.strip():
                messages.error(request, "First name and last name cannot be empty!")
            elif User.objects.filter(first_name=fn, last_name=ln).exists():
                messages.error(request, "User with this name already exists!")
            elif User.objects.filter(email=em).exists():
                messages.error(request, "User with this email already exists!")
            else:
                try:
                    reg = User(first_name=fn, last_name=ln, email=em, username=em, is_staff=True)  # Admin access
                    reg.set_password(pw)
                    reg.save()
                    messages.success(request, "User added successfully!")
                    return redirect('/addandshow/')
                except IntegrityError:
                    messages.error(request, "Error: Duplicate entry detected.")
                except Exception as e:
                    messages.error(request, f"Unexpected error: {e}")

    else:
        fm = Travel_Registration()

    # Fetch users and combine their first and last names
    hods = User.objects.all()
    users_with_full_names = [{'id': user.id, 'name': f"{user.first_name} {user.last_name}", 'email': user.email} for user in hods]

    return render(request, 'add_user/addandshow.html', {'form': fm, 'hods': users_with_full_names})
def update_data(request, id):
    pi = get_object_or_404(User, pk=id)  
    
    if request.method == 'POST':
        fm = Travel_Registration(request.POST, instance=pi)  
        if fm.is_valid():
            fm.save()
            return redirect('/')  
    else:
        fm = Travel_Registration(instance=pi)  
    
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
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        
        # Here, we assume the mobile number is being used as the username.
        try:
            user = User.objects.get(mobile_number=mobile_number)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
                user = None
        if user is not None:
            login(request, user)
            return redirect('dashboard_page')  # Redirect to your homepage or dashboard.
        else:
            messages.error(request, 'Invalid mobile number or password.')
    return render(request, 'add_user/login.html')  # Correct template path


User = get_user_model()


def SignupPage(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check required fields
        if not mobile_number:
            messages.error(request, "Mobile number is required.")
            return render(request, 'add_user/signup.html')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'add_user/signup.html')

        # Check if a user with this mobile number already exists
        if User.objects.filter(mobile_number=mobile_number).exists():
            messages.info(request, "An account with this mobile number already exists. Please log in instead.")
            return redirect('login')  # Or render a page informing them to log in

        # If not, create a new user
        try:
            User.objects.create_user(
            username="user_" + mobile_number,  # Auto-generate a username from mobile_number
            mobile_number=mobile_number,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
            messages.success(request, "User created successfully. Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            return render(request, 'add_user/signup.html')
    return render(request, 'add_user/signup.html')


#  Logout View
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


def Home(request):
    return render(request, 'add_user/home.html')  # Load home.html

 
# @login_required
# def dashboard(request):
#     users = User.objects.order_by('-date_joined')[:5]  # Get last 5 users
#     return render(request, 'add_user/dashboard.html', {'users': users})
@login_required
def dashboard(request):
    user = request.user  # Get logged-in user info
    updates = [
        "🔔 Hiking event on March 15th - Register now!",
        "🏨 20% discount on hotel bookings this weekend!"
    ]

    return render(request, 'add_user/dashboard.html', {'user': user, 'updates': updates})
@login_required
def update_profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})

def users(request):
    return render(request, 'users.html')  # Loads the users page

def settings(request):
    return render(request, 'settings.html')  # Loads the settings page
 

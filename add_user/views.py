from django.shortcuts import render, redirect , HttpResponse
from .forms import Travel_Registration
from django.db import IntegrityError 
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

def add_show(request):
    if request.method == 'POST':
        print("Request POST Data:", request.POST)  # Debugging

        fm = Travel_Registration(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']
            
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
        fm = Travel_Registration()

    hods = User.objects.all()
    return render(request, 'add_user/addandshow.html', {'form': fm, 'hod': hods})


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
        user = authenticate(request, username=mobile_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to your homepage or dashboard.
        else:
            messages.error(request, 'Invalid mobile number or password.')
    return render(request, 'add_user/login.html')  # Correct template path


User = get_user_model()

# def SignupPage(request):
#     if request.method == 'POST':
#         print("DEBUG POST:", request.POST)

#         # Get user details from the form.
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         nationality = request.POST.get('nationality')
#         city = request.POST.get('city')
#         postal_address = request.POST.get('postal_address')
#         mobile_number = request.POST.get('mobile_number').strip() # Use consistent variable name
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
#         travel_season = request.POST.get('travel_season')
#         travel_type = request.POST.get('travel_type')
#         age_range = request.POST.get('age_range')
#         budget_range = request.POST.get('budget_range')
#         print(f"Submitted mobile number: '{mobile_number}'") 
#         # Basic validation.
#         if password != confirm_password:
#             messages.error(request, "Passwords do not match.")
#             return render(request, 'add_user/signup.html')

#         if User.objects.filter(email=email).exists():
#             messages.error(request, "A user with this email already exists.")
#             return render(request, 'add_user/signup.html')

#         if User.objects.filter(username=mobile_number).exists():
#             messages.error(request, "A user with this mobile number already exists.")
#             return render(request, 'add_user/signup.html')
#         #  Check if a user with the given mobile number already exists

#         # Create the user (using mobile_number as the username).
#         user = User.objects.create_user(
#             mobile_number=mobile_number, 
#             password=password,
#             email=email,
#             first_name=first_name,
#             last_name=last_name
#         )

#         messages.success(request, "User created successfully. Please log in.")
#         return redirect('login')  # Redirect to the login page after successful signup.
    
#     return render(request, 'add_user/signup.html')
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

# @staff_member_required
# def custom_admin_dashboard(request):
#     return render(request, 'admin/dashboard.html')
# *********************************************************new **************************88
#  Logout View
@login_required
def LogoutPage(request):
    logout(request)
    return redirect('/')  # Redirect to login page after logout

# Home Page (Protected)
# @login_required
# def Home(request):
#     return render(request, 'home.html')  # Load home.html

# def dashboard(request):
#     return render(request, 'add_user/home.html')  # Loads the dashboard page
 
@login_required
def dashboard(request):
    users = User.objects.order_by('-date_joined')[:5]  # Get last 5 users
    return render(request, 'add_user/dashboard.html', {'users': users})


def users(request):
    return render(request, 'users.html')  # Loads the users page

def settings(request):
    return render(request, 'settings.html')  # Loads the settings page
 

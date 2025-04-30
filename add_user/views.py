from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .forms import Travel_Registration, UserUpdateForm, EditProfileForm, UserEditForm, TravelSchedule, ScheduleEntryForm, TravelScheduleForm
from .models import Location, Event, TravelTip, Interest, Hotel
from .utils import get_duffel_schedules
from django.core.validators import validate_email, ValidationError
from django.conf import settings
from django import forms
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HotelSerializer
User = get_user_model()
import requests
import datetime

def add_show(request):
    if request.method == 'POST':
        print("Request POST Data:", request.POST)  # Debugging

        fm = Travel_Registration(request.POST)
        if fm.is_valid():
            fn = fm.cleaned_data['first_name'].strip()
            ln = fm.cleaned_data['last_name'].strip()
            em = fm.cleaned_data['email'].strip().lower()
            pw = fm.cleaned_data['password']
            mn = fm.cleaned_data['mobile_number'].strip()

            full_name = f"{fn} {ln}".strip()

            if not fn or not ln:
                messages.error(request, "First name and last name cannot be empty!")
            elif User.objects.filter(first_name=fn, last_name=ln).exists():
                messages.error(request, "User with this name already exists!")
            elif User.objects.filter(email=em).exists():
                messages.error(request, "User with this email already exists!")
            elif User.objects.filter(mobile_number=mn).exists():
                messages.error(request, "User with this mobile number already exists!")
            else:
                try:
                    reg = User(
                        first_name=fn,
                        last_name=ln,
                        email=em,
                        username=em,
                        mobile_number=mn,
                        is_staff=True
                    )
                    reg.set_password(pw)
                    reg.save()
                    messages.success(request, "User added successfully!")
                    return redirect('/addandshow/')
                except IntegrityError as e:
                    print("IntegrityError:", e)
                    messages.error(request, f"Integrity error: {str(e)}")
                except Exception as e:
                    messages.error(request, f"Unexpected error: {e}")
        else:
            messages.error(request, "Form is invalid. Please correct the errors.")

    else:
        fm = Travel_Registration()

    # Fetch users and combine their first and last names
    hods = User.objects.all()
    users_with_full_names = [
        {
            'id': user.id,
            'name': f"{user.first_name} {user.last_name}".strip(),
            'email': user.email
        }
        for user in hods
    ]

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
# User = get_user_model()
class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())

# In your view
def LoginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']
            user = None

            try:
                if identifier.isdigit():
                    user = User.objects.get(mobile_number=identifier)
                else:
                    user = User.objects.get(username=identifier)
                
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect('/addandshow/')
                else:
                    return redirect('dashboard_page')
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = LoginForm()

    return render(request, 'add_user/login.html', {'form': form})


# views.py
def SignupPage(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        preferred_season = request.POST.get('preferred_season')
        preferred_travel_type = request.POST.get('preferred_travel_type', '').strip()
        age_range = request.POST.get('age_range', '').strip()
        budget_range = request.POST.get('budget_range', '').strip()

        # Validation
        if not mobile_number:
            messages.error(request, "Mobile number is required.")
            return render(request, 'add_user/signup.html')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'add_user/signup.html')

        if not re.match(r'^[\d\+\-\(\)\s]+$', mobile_number):
            messages.error(request, "Invalid mobile number format.")
            return render(request, 'add_user/signup.html')

        if User.objects.filter(mobile_number=mobile_number).exists():
            messages.info(request, "An account with this mobile number already exists.")
            return redirect('login')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render(request, 'add_user/signup.html')

        try:
            # Create user
            user = User.objects.create_user(
                username="user_" + mobile_number,
                mobile_number=mobile_number,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                preferred_season=preferred_season,
                preferred_travel_type=preferred_travel_type,
            )

            if hasattr(user, 'profile'):
                user.profile.age_range = age_range
                user.profile.budget_range = budget_range
                user.profile.save()

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
    offers = get_duffel_schedules()  # Fetch flight offers
    hotels = Hotel.objects.all()      # Fetch all hotels
    season = get_current_season()     # Get current season

    seasonal_destinations = Location.objects.filter(season=season)  # Fetch destinations for the season

    for destination in seasonal_destinations:
        destination.activities_list = destination.activities.split(',')

    context = {
        'flight_offers': offers,
        'hotels': hotels,
        'seasonal_destinations': seasonal_destinations,
        'current_season': season,
    }
    
    return render(request, 'add_user/home.html', context)

 
# @login_required

@login_required
def dashboard_page(request):
    user = request.user

    # Fetch recommended locations based on the user's preferred season
    recommended_locations = Location.objects.filter(season=user.preferred_season)

    # Fetch travel tips based on the user's preferences
    travel_tips = TravelTip.objects.filter(
        season=user.preferred_season,
        travel_type=user.preferred_travel_type
    )
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard_page')
    else:
        form = UserEditForm(instance=user)
    # Fetch the user's travel schedules
    schedules = TravelSchedule.objects.filter(user=user)
    schedule_form = TravelScheduleForm()
    entry_form = ScheduleEntryForm()

    if request.method == 'POST':
        if 'create_schedule' in request.POST:
            schedule_form = TravelScheduleForm(request.POST)
            if schedule_form.is_valid():
                schedule = schedule_form.save(commit=False)
                schedule.user = user
                schedule.save()
                return redirect('dashboard_page')
        elif 'add_entry' in request.POST:
            entry_form = ScheduleEntryForm(request.POST)
            schedule_id = request.POST.get('schedule_id')
            schedule = TravelSchedule.objects.get(id=schedule_id, user=user)
            if entry_form.is_valid():
                entry = entry_form.save(commit=False)
                entry.schedule = schedule
                entry.save()
                return redirect('dashboard_page')
    upcoming_events = Event.objects.filter(
        season=user.preferred_season,  # Only events after the current date
    )
    context = {
        'recommended_locations': recommended_locations,
        'travel_tips': travel_tips,
        'upcoming_events': upcoming_events,
        'form': form,
        'schedules': schedules,
        'schedule_form': schedule_form,
        'entry_form': entry_form,
    }
    return render(request, 'add_user/dashboard.html', context)


def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'update_profile.html', {'form': form})

def users(request):
    return render(request, 'users.html')  # Loads the users page

def settings(request):
    return render(request, 'settings.html')  # Loads the settings page
 
def get_interest_info(request):
    if request.method in ['GET', 'POST']:
        query = request.GET.get('query', '').strip().lower() if request.method == 'GET' else request.POST.get('query', '').strip().lower()
        print(f"Received query: '{query}'")

        suggestions = []
        recommendations = []

        # Predefined list of categories (in lowercase)
        predefined_categories = ['snow', 'mountains', 'waterfalls', 'lakes', 'greenery', 'forests', 'desert']

        # Check if query matches one of the predefined categories
        if query in predefined_categories:
            # Query matches a category
            print(f"Query matches predefined category: {query}")
            interests = Interest.objects.filter(
                Q(category__name__iexact=query)
            ).distinct()
            print(f"Filtered interests for category '{query}': {interests}")
        else:
            # If the query doesn't match a category, search by place names
            interests = Interest.objects.filter(
                Q(name__icontains=query)
            ).distinct()
            print(f"Filtered interests for name containing '{query}': {interests}")

        # Get the names of the filtered interests
        suggestions = list(set([interest.name for interest in interests]))
        print(f"Suggestions after filtering: {suggestions}")

        # Get recommendations from predefined categories (narrowed by query)
        recommendations = list(set(get_recommendations(query)))
        print(f"Recommendations after filtering: {recommendations}")

        # Return both suggestions and recommendations as JSON response
        return JsonResponse({
            'suggestions': suggestions,
            'recommendations': recommendations,
            'message': '' if (suggestions or recommendations) else 'No suggestions or recommendations found.'
        })


def get_recommendations(query):
    print(f"Processing recommendations for query: '{query}'")
    
    # Dictionary of category-based recommendations
    recommendations = {
        "snow": [
            "Murree", "Naran Kaghan", "Gilgit-Baltistan", "Malam Jabba", "Kaghan Valley",
            "Azad Kashmir", "Swat Valley", "Ziarat", "Khunjerab Pass"
        ],
        "greenery": [
            "Islamabad", "Murree", "Fairy Meadows", "Shogran", "Hunza Valley", "Naran Kaghan",
            "Neelum Valley", "Swat Valley", "Kaghan Valley", "Ratti Gali Lake"
        ],
        "mountains": [
            "Hunza Valley", "Gilgit-Baltistan", "Murree", "Kaghan Valley", "Naltar Valley",
            "Khunjerab Pass", "Deosai National Park", "Ratti Gali Lake", "Babusar Pass"
        ],
        "lakes": [
            "Saif ul Malook", "Ratti Gali Lake", "Attabad Lake", "Shandur Lake", "Keel Lake",
            "Kund Malir", "Kaghan Lake", "Lulusar Lake", "Naltar Lake"
        ],
        "waterfalls": [
            "Dhani Waterfall (Faisalabad)", "Malam Jabba Waterfalls", "Toli Pir Waterfall (Rawalakot)",
            "Dhani Waterfall (Neelum Valley)", "Nuranang Waterfall (Kaghan Valley)", "Manthoka Waterfall (Skardu)",
            "Ratti Gali Waterfall", "Torkham Waterfall (Khyber Pakhtunkhwa)", "Banjosa Waterfall (Rawalakot)",
            "Shounter Waterfall (Azad Kashmir)"
        ],
        "desert": [
            "Thar Desert", "Cholistan Desert", "Kharan Desert", "Dasht-e-Margo", "Rohi Desert", "Mekran Coast"
        ],
        "forests": [
            "Changa Manga", "Kaghan Valley", "Balochistan Forests", "Margalla Hills", "Kashmir Forests",
            "Shogran", "Fairy Meadows", "Neelum Valley"
        ]
    }
    
    # Normalize the query
    query = query.lower().strip()
    
    matched = set()

    # Check if the query matches a category exactly
    if query in recommendations:
        matched.update(recommendations[query])  # Add all places from that category
    else:
        # If not, check if it matches any place name (case insensitive)
        for category, places in recommendations.items():
            for place in places:
                if query in place.lower():  # Check if query matches part of the place name
                    matched.add(place)
    
    return list(matched)
def get_suggestions(query):
    # Example list of suggestions (can be replaced with database query or more complex logic)
    all_suggestions = [
        'Mountains', 'Lakes', 'Beaches', 'Forests', 'Deserts', 'Snow', 'Rivers', 'Volcanoes'
    ]
    
    # Filter suggestions based on the query
    return [sug for sug in all_suggestions if query in sug.lower()]
# Your Django view
def interest_page(request):
    query = request.GET.get('query', '').strip().lower()

    # Get suggestions and recommendations based on the query
    suggestions = get_suggestions(query)  # logic to fetch suggestions
    recommendations = get_recommendations(query)  # to fetch recommendations

    # Return both suggestions and recommendations as a JSON response
    return JsonResponse({
        'suggestions': suggestions,
        'recommendations': recommendations
    })

class HotelListAPIView(APIView):
    def get(self, request):
        city = request.GET.get('city')
        hotels = Hotel.objects.all()
        if city:
            hotels = hotels.filter(city__iexact=city)
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

def get_current_season():
    month = datetime.datetime.now().month
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Autumn'
    
@login_required
def create_schedule(request):
    if request.method == 'POST':
        form = TravelScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            return redirect('add_schedule_entry', schedule_id=schedule.id)
    else:
        form = TravelScheduleForm()
    return render(request, 'add_user/create_schedule.html', {'form': form})

@login_required
def add_schedule_entry(request, schedule_id):
    schedule = TravelSchedule.objects.get(id=schedule_id, user=request.user)
    if request.method == 'POST':
        form = ScheduleEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.schedule = schedule
            entry.save()
            return redirect('add_schedule_entry', schedule_id=schedule.id)
    else:
        form = ScheduleEntryForm()
    entries = schedule.entries.all()
    return render(request, 'add_user/add_schedule_entry.html', {'form': form, 'entries': entries, 'schedule': schedule})


def delete_schedule(request, schedule_id):
    if request.method == 'POST':
        schedule = get_object_or_404(TravelSchedule, pk=schedule_id)
        schedule.delete()
    return redirect('your_dashboard_view_name')
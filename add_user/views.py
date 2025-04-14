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
from .models import Location, Event, TravelTip
from .models import Interest, UserActivity
from .forms import InterestSearchForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# def add_show(request):
#     if request.method == 'POST':
#         print("Request POST Data:", request.POST)  # Debugging

#         fm = Travel_Registration(request.POST)
#         if fm.is_valid():
#             fn = fm.cleaned_data['first_name']
#             ln = fm.cleaned_data['last_name']
#             em = fm.cleaned_data['email']
#             pw = fm.cleaned_data['password']

#             full_name = f"{fn} {ln}".strip()

#             if not fn.strip() or not ln.strip():
#                 messages.error(request, "First name and last name cannot be empty!")
#             elif User.objects.filter(first_name=fn, last_name=ln).exists():
#                 messages.error(request, "User with this name already exists!")
#             elif User.objects.filter(email=em).exists():
#                 messages.error(request, "User with this email already exists!")
#             else:
#                 try:
#                     reg = User(first_name=fn, last_name=ln, email=em, username=em, is_staff=True)  # Admin access
#                     reg.set_password(pw)
#                     reg.save()
#                     messages.success(request, "User added successfully!")
#                     return redirect('/addandshow/')
#                 except IntegrityError as e:
#                     print("IntegrityError:", e)  # Add this line
#                     messages.error(request, f"Integrity error: {str(e)}")
#                 except Exception as e:
#                     messages.error(request, f"Unexpected error: {e}")

#     else:
#         fm = Travel_Registration()

#     # Fetch users and combine their first and last names
#     hods = User.objects.all()
#     users_with_full_names = [{'id': user.id, 'name': f"{user.first_name} {user.last_name}", 'email': user.email} for user in hods]

#     return render(request, 'add_user/addandshow.html', {'form': fm, 'hods': users_with_full_names})
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
def LoginPage(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # Can be mobile number or username
        password = request.POST.get('password')

        user = None

        # Check if input is a mobile number or a username
        try:
            if identifier.isdigit():  # Assuming mobile numbers are numeric
                user = User.objects.get(mobile_number=identifier)
            else:
                user = User.objects.get(username=identifier)
            
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            if user.is_staff:  # Admin user
                return redirect('/addandshow/')  # Redirect admin to admin page
            else:
                return redirect('dashboard_page')  # Redirect regular users to dashboard
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'add_user/login.html')


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
@login_required
def dashboard(request):
    suggested_locations = [
        {"name": "Swiss Alps", "description": "Perfect for winter sports and scenic views."},
        {"name": "Bali, Indonesia", "description": "A tropical paradise with beautiful beaches and temples."},
        {"name": "Paris, France", "description": "A cultural hub with historical landmarks and fine dining."}
    ]

    # Sample upcoming events
    suggested_events = [
        {"title": "Hiking Adventure in the Rockies", "date": "March 20, 2025", "description": "Join an exciting hiking experience in the Rocky Mountains."},
        {"title": "Cherry Blossom Festival, Japan", "date": "April 5, 2025", "description": "Enjoy the breathtaking cherry blossoms in full bloom."},
        {"title": "Safari Experience in Kenya", "date": "June 10, 2025", "description": "Explore the wildlife and natural beauty of Africa."}
    ]

    # Sample travel tips
    suggested_tips = [
        {"title": "Packing Essentials", "content": "Always carry a power bank, first-aid kit, and travel adapter."},
        {"title": "Budget Travel", "content": "Use public transport and book accommodations in advance for discounts."},
        {"title": "Safety Tips", "content": "Keep digital copies of important documents and be aware of your surroundings."}
    ]

    return render(request, 'add_user/dashboard.html', {
        "suggested_locations": suggested_locations,
        "suggested_events": suggested_events,
        "suggested_tips": suggested_tips
    })

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
    suggestions = get_suggestions(query)  # Your logic to fetch suggestions
    recommendations = get_recommendations(query)  # Your logic to fetch recommendations

    # Return both suggestions and recommendations as a JSON response
    return JsonResponse({
        'suggestions': suggestions,
        'recommendations': recommendations
    })



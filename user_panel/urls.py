"""
URL configuration for user_panel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from add_user import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginPage, name='login'), 
    path('', views.SignupPage, name='signup'),  
    path('home/', views.Home, name='home'),
    path('addandshow/', views.add_show, name="addandshow"),
    path('delete/<int:id>/', views.delete_data, name="deletedata"),
    path('update/<int:id>/', views.update_data, name="updatedata"),
    path('dashboard/', views.dashboard_page, name="dashboard_page"),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('interests/', views.get_interest_info, name='get_interest_info'),
    path('/', views.get_recommendations, name='get_recommendations'),
    path('interest_page/', views.interest_page, name='interest_page'),
    path('api/hotels/', views.HotelListAPIView.as_view(), name='hotel-list'),
    path('schedule/delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('book-flight/', views.book_flight, name='book_flight'),
    path('cancel-flight/', views.cancel_flight, name='cancel_flight'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# from django.shortcuts import render
# from .forms import Hod_Registration
# from .models import User

# # Create your views here.
# def add_show(request):
#     if request.method == 'POST':
#         fm = Hod_Registration(request.POST)
#         if fm.is_valid():
#             nm = fm.cleaned_data['name']
#             em = fm.cleaned_data['email']
#             pw = fm.cleaned_data['password']
#             reg = User(name=nm, email=em, password =pw)
#             reg.save()
#             fm = Hod_Registration()
#     else:
#         fm = Hod_Registration()
#         hods = User.objects.all()
# return render(request, 'add_user/addandshow.html', {'form': fm, 'hod': hods})
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import Hod_Registration
from django.shortcuts import render, redirect, get_object_or_404
from .models import User


# this fucntion will add new item and show all items 
def add_show(request):
    if request.method == 'POST':
        fm = Hod_Registration(request.POST)
        if fm.is_valid():
            nm = fm.cleaned_data['name']
            em = fm.cleaned_data['email']
            pw = fm.cleaned_data['password']
            reg = User(name=nm, email=em, password=pw)
            reg.save()
            return redirect('/')  
    else:
        fm = Hod_Registration()
        hods = User.objects.all()
        return render(request, 'add_user/addandshow.html', {'form': fm, 'hod': hods})
    

# This function will update data
# def update_data(request, id):
#     if request.method == 'POST':
#         pi =User.objects.get(pk=id)
#         fm = Hod_Registration(request.POST, instance=pi)
#         if fm.is_valid():
#             fm.save()
#     else:
#         pi =User.objects.get(pk=id)
#         fm = Hod_Registration(request.POST, instance=pi)
    
#  return render(request, 'add_user/updateuser.html', {'form': fm})

def update_data(request, id):
    pi = get_object_or_404(User, pk=id)  
    
    if request.method == 'POST':
        fm = Hod_Registration(request.POST, instance=pi)  
        if fm.is_valid():
            fm.save()
            return redirect('success_page')  
    else:
        fm = Hod_Registration(instance=pi)  
    
    return render(request, 'add_user/updateuser.html', {'form': fm})  


# This function will delete data

def delete_data(request, id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/')
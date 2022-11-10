from django.shortcuts import render,redirect
from .forms import UserForm
from .models import User
from django.contrib import messages
# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Method 1 to save the password in hash format
            password = form.cleaned_data['password']
            user=form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,"User have been registered")
            return redirect('registerUser')
            
            # Method 1 to save the password in hash format
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # username = form.cleaned_data['username']
            # password = form.cleaned_data['password']
            
            # user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            # user.role = User.CUSTOMER
            # user.save()
            # return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form' : form
    }
    return render(request,'accounts/registerUser.html',context)
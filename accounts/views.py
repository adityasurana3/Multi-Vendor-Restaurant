from django.shortcuts import render,redirect
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages, auth
from vendor.forms import VendorForm
from .utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor
from django.template.defaultfilters import slugify
from orders.models import Order
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import datetime

# Create your views here.

# Restrict the customer from accessing the vendor page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
# Restrict the vendor from accessing the customer page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You're already loggedin")
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Method 1 to save the password in hash format
            password = form.cleaned_data['password']
            user=form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()
            mail_subject = 'Please click on the link to activate your account'
            email_template ='accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,"User have been registered. Please check your email to activate your account")
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

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,"You're already loggedin")
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            mail_subject = 'Please click on the link to activate your account'
            email_template ='accounts/emails/account_verification_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,'Your account have been register successfully! Please wait for the approval')
            return redirect('registerVendor')
        else:
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()
    context = {
        'form':form,
        'v_form':v_form
    }
    return render(request,'accounts/registerVendor.html',context=context)

def activate(request,uidb64,token):
    # Activating the user by setting is_active as True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Congratulation! Your account has been activated")
        return redirect('myAccount')
    else:
        messages.error(request,"Invalid activation link")
        return redirect('myAccount')

def login(request):
    if request.user.is_authenticated:
        messages.warning(request,"You're already loggedin")
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"You are logged in")
            return redirect('myAccount')
        else:
            messages.error(request,"Invalid Credential")
            return redirect('login')
    return render(request,'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"You are logged out")
    return redirect('login')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    orders = Order.objects.filter(user=request.user,is_ordered = True)
    recent_orders = orders[:5]
    context = {
        'orders':orders,
        'orders_count':orders.count(),
        'recent_orders':recent_orders,
    }
    return render(request,'accounts/custDashboard.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    vendor = Vendor.objects.get(user = request.user)
    orders = Order.objects.filter(vendors__in = [vendor.id], is_ordered = True).order_by('-created_at')
    recent_orders = orders[:5]

    # current months revenue
    current_month = datetime.datetime.now().month
    current_month_order = orders.filter(vendors__in=[vendor.id],created_at__month = current_month)
    current_month_revenue = 0
    for i in current_month_order:
        current_month_revenue += i.get_total_by_vendor()['grand_total']

    # total_revenue
    total_revenue = 0
    for i in orders:
        total_revenue += i.get_total_by_vendor()['grand_total']
    context = {
        'orders':orders,
        'order_count':orders.count(),
        'recent_orders':recent_orders,
        'total_revenue':total_revenue,
        'current_month_revenue':current_month_revenue,
    }
    return render(request,'accounts/vendorDashboard.html', context)

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email):
            user = User.objects.get(email__exact = email)
            mail_subject = 'Password reset link has been sent to your email address.'
            email_template ='accounts/emails/reset_password_email.html'
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,"Email has been sent")
            return redirect('login')
            
        else:
            messages.error(request,"Account does not exist")
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request,'This link has been expired')
        return redirect('myAccount')
        

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request,'Password reset successfully')
            return redirect('login')
        else:
            messages.error(request,'Password did not match')
            return redirect('reset_password')
    return render(request,'accounts/reset_password.html')

@login_required(login_url='login')
def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user = request.user, data = request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password changed successfully')
                return redirect('custDashboard')
        else:
            form  = PasswordChangeForm(user = request.user)
        context = {
            'form':form
        }
        return render(request, 'accounts/change_password.html' ,context)
    else:
        return redirect('login')
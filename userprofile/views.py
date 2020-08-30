from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from cart.models import Order,OrderItem,CheckoutInfo
from django.contrib.auth.decorators import login_required
from product.models import ProductComment
from .forms import FirstLastNameForm,EmailForm,PhoneForm,BirthDateForm,ImageForm
from .models import UserProfile
# Create your views here.

@login_required
def userprofile (request):

    # user_id=request.user.id
    # current_user=get_object_or_404(User,id=pk)
    orders=Order.objects.filter(user=request.user)
    context={
        # 'current_user': current_user,
        'orders':orders
    }
    return render(request,'profile_page.html',context)

@login_required
def OrderDetail(request,pk):
    userorder=get_object_or_404(Order,id=pk)
    orderitems=OrderItem.objects.filter(order=userorder)
    context={
        'userorder':userorder,
        'orderitems':orderitems
    }
    return render(request,'order-detail.html',context)

@login_required
def UserOrders(request):
    userorders=Order.objects.filter(user=request.user)
    context={
        'userorders':userorders
    }
    return render(request,'userorders.html',context)

@login_required
def UserAddresses(request):
    infos=CheckoutInfo.objects.filter(user=request.user)
    context={
        'infos': infos
    }
    return render(request,'user-address.html',context)

@login_required
def UserComments(request):
    comments=ProductComment.objects.filter(user=request.user)
    context={
        'comments': comments
    }
    return render(request,'user-comments.html',context)

@login_required
def PersonalInfo(request):
    if request.method == "POST":
        name_form = FirstLastNameForm(request.POST or None)
        email_form=EmailForm(request.POST or None)
        phone_form=PhoneForm(request.POST or None)
        birth_date_form=BirthDateForm(request.POST or None)
        image_form=ImageForm(request.POST ,request.FILES)
        if name_form.is_valid():
            first_name = name_form.cleaned_data.get('first_name')
            last_name=name_form.cleaned_data.get('last_name')
            if UserProfile.objects.filter(user=request.user).exists():
                userprofile=UserProfile.objects.get(user=request.user)
                userprofile.first_name=first_name
                userprofile.last_name=last_name
                userprofile.save()
        if email_form.is_valid():
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.email = email_form.cleaned_data.get('email')
            userprofile.save() 
        if phone_form.is_valid():
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.phone_number = phone_form.cleaned_data.get('phone_number')
            userprofile.save()
        if birth_date_form.is_valid():
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.birth_date = birth_date_form.cleaned_data.get('birth_date')
            userprofile.save() 
        if image_form.is_valid():
            userprofile=UserProfile.objects.get(user=request.user)
            userprofile.avatar = image_form.cleaned_data.get('image')
            userprofile.save()
    else:
        name_form = FirstLastNameForm()
        email_form=EmailForm()
        phone_form=PhoneForm()
        birth_date_form=BirthDateForm()
        image_form=ImageForm()
    context={
        'name_form':FirstLastNameForm(initial={
            'first_name':request.user.userprofile.first_name,
            'last_name':request.user.userprofile.last_name    
        }),
        'email_form':EmailForm(initial={
            'email':request.user.userprofile.email,
        }),
        'phone_form':PhoneForm(initial={
            'phone_number':request.user.userprofile.phone_number,
        }),
        'birth_date_form':BirthDateForm(),
        'image_form':ImageForm(),
    }
    return render(request,'personal-info.html',context)

def datepicker(request):
    return render(request,'datepicker.html',{})
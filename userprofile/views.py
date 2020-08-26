from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from cart.models import Order

# Create your views here.
def userprofile (request,pk):
    if request.user.is_authenticated:
        user_id=request.user.id
        current_user=get_object_or_404(User,id=pk)
        orders=Order.objects.filter(user=current_user)
        context={
            'current_user': current_user,
            'orders':orders
        }
        return render(request,'profile_page.html',context)
    else:
        return redirect('/accounts/login')
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from cart.models import Order,OrderItem,CheckoutInfo
from django.contrib.auth.decorators import login_required
from product.models import ProductComment

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

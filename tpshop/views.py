from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib import messages

def home(request):
    context={
    'name':'Ebrahim'
    }
    return render(request, 'index.html', context)
    
def auth_login(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid :
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    
    form = LoginForm()
    return render(request = request,
                  template_name = "login.html",
                  context={"form":form})


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        pass
    form = RegisterForm()
    return render(request, "register.html", context ={"form": form})

        
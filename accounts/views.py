from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import login, logout, authenticate

# Register a new user.
def register(request):
    if request.user.is_authenticated:
        return redirect("review:home")

    #if the user is not logged in
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST or None)

            #check if the form is valid
            if form.is_valid():
                user = form.save()
                raw_password = form.cleaned_data.get('password1')

                #authenticate the user
                user = authenticate(username = user.username, password = raw_password)

                #login the user
                login(request, user)
                return redirect("review:home")

        else:
            form = RegistrationForm()
        return render(request,"accounts/register.html",{"form":form})

#login the registered user
def login_user(request):
    if request.user.is_authenticated:
        return redirect("review:home")

    #if the user is not logged in
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            #verify the credentials
            user = authenticate(username = username, password = password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("review:home")
                else:
                    return render(request,"accounts/login.html", {"error": "Your account has been disabled"})

        else:
            return render(request, "accounts/login.html",{"error":"Invalid username or password"})
        return render(request, "accounts/login.html")

#logout user
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("accounts:login")
    else:
        return redirect("accounts:login")



from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'index.html', {'fname': fname})

def urlPage(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'urlPage.html', {'fname': fname})

def document(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'document.html', {'fname': fname})

def audio(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'audio.html', {'fname': fname})

def signin(request):

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]

        user = authenticate(username=username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'index.html', {'fname': fname})
            # return redirect("home")
        else:
            messages.error(request, "Bad credentials!")
            return redirect("signin")

    return render(request, 'signin.html', {})

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been successfully created.")

        return redirect("signin")

    return render(request, 'signup.html', {})

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("home")

from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from transformers import pipeline, AutoTokenizer


def home(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        tokenizer_path = "D:/python/NLP/django_text-summarize/text_summarizer/website/model/tokenizer-summarization"
        model_path = "Falconsai/text_summarization"
        # tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        summarizer = pipeline("summarization", model=model_path, framework='tf')
        summary = summarizer(input_text, max_length=1000, min_length=30, do_sample=False)
        summarized_text = summary[0]['summary_text']
        return render(request, 'index.html', {'summarized_text': summarized_text, 'input_text': input_text, 'fname': fname})
    else:
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
  

def test(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        tokenizer_path = "D:/python/NLP/django_text-summarize/text_summarizer/website/model/tokenizer-summarization"
        model_path = "D:/python/NLP/django_text-summarize/text_summarizer/website/model/pegasus-samsum-model"
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        summarizer = pipeline("summarization", model=model_path,tokenizer=tokenizer, framework='tf')
        summary = summarizer(input_text, length_penalty= 0.8, num_beams=8, max_length= 1028)
        summarized_text = summary[0]['summary_text']
        return render(request, 'test.html', {'summarized_text': summarized_text})
    else:
        return render(request, 'test.html', {})

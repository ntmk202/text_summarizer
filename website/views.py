from django.shortcuts import render

def home(request):
    return render(request, 'index.html', {})

def urlPage(request):
    return render(request, 'urlPage.html', {})

def document(request):
    return render(request, 'document.html', {})

def audio(request):
    return render(request, 'audio.html', {})


from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from transformers import pipeline, AutoTokenizer
from .models import Summary
from datetime import date
from itertools import groupby
from django.shortcuts import get_object_or_404
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, NoTranscriptAvailable
import re

def home(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        tokenizer_path = "D:/python/NLP/django_text-summarize/text_summarizer/website/model/tokenizer-summarization"
        model_path = "D:/python/NLP/django_text-summarize/text_summarizer/website/model/pegasus-samsum-model"
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        summarizer = pipeline("summarization", model=model_path,tokenizer=tokenizer, framework='tf')
        summary = summarizer(input_text, length_penalty= 0.8, num_beams=8, max_length= 1028)
        summarized_text = summary[0]['summary_text']

        if request.user.is_authenticated:
            Summary.objects.create(user=request.user, original_text=input_text, summarized_text=summarized_text)

        return render(request, 'index.html', {'summarized_text': summarized_text, 'input_text': input_text, 'fname': fname})
    else:
        return render(request, 'index.html', {'fname': fname})

def urlPage(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'urlPage.html', {'fname': fname})

def history(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    if request.user.is_authenticated:
        summaries = Summary.objects.filter(user=request.user).order_by('-created_at')
        grouped_summaries = {}
        for key, group in groupby(summaries, lambda x: x.created_at.date()):
            grouped_summaries[key] = list(group)
    else:
        grouped_summaries = {}

    return render(request, 'history.html', {'grouped_summaries': grouped_summaries, 'fname': fname})

def document(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'document.html', {'fname': fname})

COMMON_LANGUAGES = [
    ('English', 'en'),
    ('English (United Kingdom)', 'en-GB'),
    ('Spanish', 'es'),
    ('French', 'fr'),
    ('German', 'de'),
    ('Vietnamese', 'vi'),
]

def youtube_link(request):
    fname = request.user.first_name if request.user.is_authenticated else None
    available_languages = COMMON_LANGUAGES
    transcript = None
    error = None
    summarized_text = None

    if request.method == 'POST':
        youtube_link = request.POST.get('youtube_link')
        language_code = request.POST.get('language_code', 'en')
        video_id = extract_video_id(youtube_link)

        if video_id:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
                transcript_text = " ".join([t['text'] for t in transcript])
                tokenizer_path = "D:/python/NLP/django_text-summarize/text_summarizer/website/model/tokenizer-summarization"
                model_path = "D:/python/NLP/django_text-summarize/text_summarizer/website/model/pegasus-samsum-model"
                tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
                summarizer = pipeline("summarization", model=model_path,tokenizer=tokenizer, framework='tf')
                summary = summarizer(transcript_text, length_penalty= 0.8, num_beams=8, max_length= 1028)
                summarized_text = summary[0]['summary_text']
            except NoTranscriptFound as e:
                try:
                    transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
                    available_languages = [(t.language, t.language_code) for t in transcripts]
                    error = 'Please choose an available language code'
                except (TranscriptsDisabled, NoTranscriptAvailable) as e:
                    error = 'Transcripts are disabled for this video or not available.'
            except Exception as e:
                error = str(e)
        else:
            error = 'Invalid YouTube URL'

    return render(request, 'audio.html', {
        'transcript': transcript,
        'summarized_text': summarized_text,
        'fname': fname,
        'error': error,
        'available_languages': available_languages,
    })

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    """
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None


def signin(request):

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]

        user = authenticate(username=username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'index.html', {'fname': fname})
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

def summary_detail(request, id):
    fname = request.user.first_name if request.user.is_authenticated else None
    summary = get_object_or_404(Summary, id=id, user=request.user)
    return render(request, 'summary_detail.html', {'summary': summary, 'fname': fname})

def delete_summary(request, id):
    if request.user.is_authenticated:
        summary = get_object_or_404(Summary, id=id, user=request.user)
        summary.delete()
        messages.success(request, "Summary deleted successfully.")
        return redirect('history')


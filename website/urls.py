from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('urlPage', views.urlPage, name='url_Page'),
    path('document', views.document, name='document'),
    path('audio', views.audio, name='audio'),
]

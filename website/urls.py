from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('urlPage', views.urlPage, name='url_Page'),
    path('document', views.document, name='document'),
    path('audio', views.audio, name='audio'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
]

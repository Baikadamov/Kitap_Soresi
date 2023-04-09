from django.urls import path

from social_book.views import *

urlpatterns = [
    path('', feed, name='feed'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout, name='logout'),
    path('settings/', settings, name='settings'),
    # path('upload/', upload, name='upload'),
    path('upload/', upload, name='upload'),
]

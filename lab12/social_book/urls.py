from django.urls import path

from social_book.views import *

urlpatterns = [
    path('', feed, name='feed'),
    path('signup', signup, name='signup'),
    path('signin', signin, name='signin'),
    path('profile/<str:pk>', profile, name='profile'),

    path('search/city/<slug:city_slug>', show_city, name='city'),
    path('search/interest/<slug:interest_slug>', show_interest, name='interest'),




    path('post/<str:pk>', post, name='post'),
    path('logout', logout, name='logout'),
    path('settings', settings, name='settings'),
    path('like-post', like_post, name='like-post'),
    path('follow', follow, name='follow'),
    path('search', search, name='search'),
    path('upload', upload, name='upload'),
    path('deletepost', deletepost, name='deletepost'),
    path('updatepost', updatepost, name='updatepost'),
    path('addcomment', addcomment, name='addcomment'),
    path('deletecomment', deletecomment, name='deletecomment'),
    path('subs-posts', subs_posts, name='subs_posts'),
]

import random
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.db import IntegrityError
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from social_book.models import *
from social_book.serializers import *


@login_required(login_url='signin')
def feed(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    all_user = User.objects.all()
    user_following_all = []

    for user in user_following_all:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_user) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))

    posts = Post.objects.all()

    context = {
        'posts': posts,
        'user_profile': user_profile,
        'suggestions_username_profile_list': suggestions_username_profile_list[:4],
    }

    return render(request, 'social_book/feed.html', context=context)


@login_required(login_url='signin')
def subs_posts(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []

    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    posts = Post.objects.all()

    context = {
        'posts': feed_list,
        'user_profile': user_profile,
    }

    return render(request, 'social_book/subs_post.html', context=context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'social_book/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('signin')

    return render(request, 'social_book/signin.html')


def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.FILES.get('image') is None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            number = request.POST['number']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.number = number
            user_profile.save()

        if request.FILES.get('image') is not None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            number = request.POST['number']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.number = number
            user_profile.save()
        messages.info(request, 'Information updated')
        return redirect('settings')

    return render(request, 'social_book/settings.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        try:
            new_post = Post.objects.create(user=user, image=image, caption=caption)
            new_post.save()
        except IntegrityError:
            messages.error(request, 'An error occurred while saving your post. Please try again later.')
            return redirect(request.META['HTTP_REFERER'])

        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
        button_style = 'btn-danger'
    else:
        button_text = 'Follow'
        button_style = 'btn-outline-danger'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_posts_length': user_posts_length,
        'button_text': button_text,
        'button_style': button_style,
        'user_followers': user_followers,
        'user_following': user_following,
    }

    return render(request, 'social_book/profile.html', context=context)


@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/' + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/' + user)
    else:
        return render(request, 'social_book/profile.html', )


@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'social_book/search.html',
                  {'user_profile': user_profile, 'username_profile_list': username_profile_list})


def post(request, pk):
    post_detail = Post.objects.get(id=pk)

    context = {
        'post': post_detail,
    }

    return render(request, 'social_book/post.html', context)


def addcomment(request):
    if request.method == 'POST':
        user = request.user.username

        comment_body = request.POST['comment_body']
        pk = request.POST['pk']
        posts = Post.objects.get(id=pk)

        c = Comment(post=posts, commenter_name=user, comment_body=comment_body, date_added=datetime.now())
        c.save()

        print(user)
        print(comment_body)
        return redirect(request.META['HTTP_REFERER'])

    return redirect(request.META['HTTP_REFERER'], )


def deletecomment(request):
    if request.method == 'POST':
        pk = request.POST['pk']
        comment = Comment.objects.filter(id=pk)
        comment.delete()
        return redirect(request.META['HTTP_REFERER'], )
    return redirect(request.META['HTTP_REFERER'], )



class PostAPIView(APIView):

    def get(self, request):
        p = Post.objects.all()
        return Response({'posts': PostSerializer(p, many=True).data})

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method put not allowed"})

        try:
            instance = Post.objects.get(pk=pk)
        except:
            return Response({"error": "oBject doesnt not exists"})

        serializer = PostSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            record = Post.objects.get(pk=pk)
            record.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"post": "delete post " + str(pk)})


class ProfileAPIView(APIView):

    def get(self, request):
        p = Profile.objects.all()
        return Response({'profile': ProfileSerializer(p, many=True).data})

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'profile': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method put not allowed"})

        try:
            instance = Profile.objects.get(pk=pk)
        except:
            return Response({"error": "oBject doesnt not exists"})

        serializer = ProfileSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            record = Profile.objects.get(pk=pk)
            record.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"post": "delete post " + str(pk)})


class CommentAPIView(APIView):

    def get(self, request):
        p = Comment.objects.all()
        return Response({'comment': CommentSerializer(p, many=True).data})

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'comment': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method put not allowed"})

        try:
            instance = Comment.objects.get(pk=pk)
        except:
            return Response({"error": "oBject doesnt not exists"})

        serializer = CommentSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Comment": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            record = Comment.objects.get(pk=pk)
            record.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"post": "delete post " + str(pk)})


class FollowersCountAPIView(APIView):

    def get(self, request):
        p = FollowersCount.objects.all()
        return Response({'FollowersCount': FollowersCountSerializer(p, many=True).data})

    def post(self, request):
        serializer = FollowersCountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'FollowersCount': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method put not allowed"})

        try:
            instance = FollowersCount.objects.get(pk=pk)
        except:
            return Response({"error": "oBject doesnt not exists"})

        serializer = FollowersCountSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"FollowersCount": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            record = FollowersCount.objects.get(pk=pk)
            record.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"post": "delete post " + str(pk)})

class LikePostAPIView(APIView):

    def get(self, request):
        p = LikePost.objects.all()
        return Response({'LikePost': LikePostSerializer(p, many=True).data})

    def post(self, request):
        serializer = LikePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'LikePost': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method put not allowed"})

        try:
            instance = LikePostSerializer.objects.get(pk=pk)
        except:
            return Response({"error": "oBject doesnt not exists"})

        serializer = LikePostSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"LikePost": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})

        try:
            record = LikePost.objects.get(pk=pk)
            record.delete()
        except:
            return Response({"error": "Object does not exists"})

        return Response({"post": "delete post " + str(pk)})

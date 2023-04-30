import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from social_book.models import *


# class PostModel:
#     def __init__(self, user, caption):
#         self.user = user
#         self.caption = caption


class PostSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)
    image = serializers.ImageField()
    caption = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    no_of_likes = serializers.IntegerField(default=0)

    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data["user"]
        instance.image = validated_data.get("image", instance.image)
        instance.caption = validated_data.get("caption", instance.caption)
        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.no_of_likes = validated_data.get("no_of_likes", instance.no_of_likes)
        instance.save()
        return instance


class ProfileSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=100)
    id_user = serializers.IntegerField()
    bio = serializers.CharField(read_only=True)
    number = serializers.CharField(read_only=True)
    profileimg = serializers.ImageField(read_only=True)
    location = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        username = validated_data["username"]
        user = get_user_model().objects.get(username=username)
        instance.user = user
        instance.id_user = validated_data.get("id_user", instance.id_user)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.number = validated_data.get("number", instance.number)
        instance.profileimg = validated_data.get("profileimg", instance.profileimg)
        instance.location = validated_data.get("location", instance.location)
        instance.save()
        return instance


class CommentSerializer(serializers.Serializer):
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    commenter_name = serializers.CharField()
    comment_body = serializers.CharField()
    date_added = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        comment = Comment.objects.create(**validated_data)
        return comment

    def update(self, instance, validated_data):
        instance.post = validated_data["post"]
        instance.commenter_name = validated_data.get("commenter_name", instance.commenter_name)
        instance.comment_body = validated_data.get("comment_body", instance.comment_body)
        instance.date_added = validated_data.get("date_added", instance.date_added)
        instance.save()
        return instance


class FollowersCountSerializer(serializers.Serializer):
    follower = serializers.CharField(max_length=100)
    user = serializers.CharField()

    def create(self, validated_data):
        return FollowersCount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.follower = validated_data["follower"]
        instance.user = validated_data.get("user", instance.user)
        instance.save()
        return instance


class LikePostSerializer(serializers.Serializer):
    post_id = serializers.CharField(max_length=100)
    username = serializers.CharField()

    def create(self, validated_data):
        return LikePost.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.post_id = validated_data["post_id"]
        instance.post_id = validated_data.get("post_id", instance.post_id)
        instance.save()
        return instance

# def encode():
#     model = PostModel('maks', 'awdwad')
#     model_sr = PostSerializer(model)
#     print(model_sr, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
#
# def decode():
#     stream = io.BytesIO(b'{"user":"maks","caption":"awdwad"}')
#     data = JSONParser().parse(stream)
#     serializer = PostSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)

from rest_framework import serializers, viewsets

from messenger.models import Books, Genre, Author
from social_book.models import *


class BooksSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Books
        fields = "__all__"


# class BooksSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=100)
#     slug = serializers.CharField()
#     author = serializers.CharField()
#     photo = serializers.ImageField()
#     description = serializers.CharField()
#     genre = serializers.CharField()
#     price = serializers.CharField()
#     is_published = serializers.BooleanField()
#
#     def create(self, validated_data):
#         return Books.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data["name"]
#         instance.slug = validated_data.get("slug", instance.slug)
#         instance.author = validated_data.get("author", instance.author)
#         instance.photo = validated_data.get("photo", instance.photo)
#         instance.description = validated_data.get("description", instance.description)
#         instance.genre = validated_data.get("genre", instance.genre)
#         instance.price = validated_data.get("price", instance.price)
#         instance.is_published = validated_data.get("is_published", instance.is_published)
#         instance.save()
#         return instance


class GenreSerializer(serializers.Serializer):
    slug = serializers.CharField()
    name = serializers.CharField()

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.slug = validated_data.get("slug", instance.slug)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class AuthorSerializer(serializers.Serializer):
    slug = serializers.CharField()
    name = serializers.CharField()

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.slug = validated_data.get("slug", instance.slug)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Movies,Reviews





class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=["id","username","email","password"]
        read_only_fields=["id"]
    
    def create(self,validated_data):
        return User.objects.create_user(**validated_data)


class ReviewSerializer(serializers.ModelSerializer):

    user=serializers.StringRelatedField()
    movie=serializers.StringRelatedField()
    class Meta:
        model=Reviews
        fields="__all__"
        read_only_fields=["id","user","movie","is_active","created_at","updated_at"]


class MovieSerializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(read_only=True,many=True)
    avg_rating=serializers.IntegerField(read_only=True)
    class Meta:
        model=Movies
        fields="__all__"
        read_only_fields=["id","avg_rating","is_active","created_at","updated_at"]


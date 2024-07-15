from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import authentication,permissions
from rest_framework.decorators import action

from api.serializers import UserSerializer,MovieSerializer,ReviewSerializer
from api.models import Movies,Reviews

# Create your views here.


class SignUpView(APIView):

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    

class MovieView(viewsets.ModelViewSet):
    serializer_class=MovieSerializer
    queryset=Movies.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    def update(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    def destroy(self, request, *args, **kwargs):
        raise serializers.ValidationError("permission denied")
    
    # url:http://127.0.0.1:8000/api/movies/{id}/add_review/
    # method:post

    @action(methods=["post"],detail=True)
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        movie_object=Movies.objects.get(id=id)
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(movie=movie_object,user=request.user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)




class ReviewView(viewsets.ViewSet):
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Reviews.objects.get(id=id)
        serializer=ReviewSerializer(qs)
        return Response(data=serializer.data)
    
    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        review_object=Reviews.objects.get(id=id)
        serializer=ReviewSerializer(data=request.data,instance=review_object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
    def destroy(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Reviews.objects.get(id=id).delete()
        return Response(data={"message":"deleted"})

from django.urls import path

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

from api import views

router=DefaultRouter()
router.register("movies",views.MovieView,basename="movies")
router.register("reviews",views.ReviewView,basename="reviews")




urlpatterns=[
    path("register/",views.SignUpView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
]+router.urls
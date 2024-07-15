from django.shortcuts import render
from django.views.generic import View

# Create your views here.

# class IndexView(View):
#     def get(self,request,*args,**kwargs):
#         print("hello")
#         return render(request,"index.html")

def home(request):
    return render(request,"app/index.html")
from django.shortcuts import render,redirect



from django.views import View
from book.models import Books
from book.forms import BookForm,RegistrationForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

# decorators

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
        




# Create your views here.
# view classes
@method_decorator(signin_required,name="dispatch")
class BookListView(View):
    def get(self,request,*args,**kwargs):
        qs=Books.objects.all()

        if "genre" in request.GET:
            genre=request.GET.get("genre")
            qs=qs.filter(genre__iexact=genre)
        
        if "publisher" in request.GET:
            publisher=request.GET.get("publisher")
            qs=qs.filter(publisher__iexact=publisher)

        if "author" in request.GET:
            author=request.GET.get("author")
            qs=qs.filter(author__iexact=author)

        if "price__lt" in request.GET:
            amount=request.GET.get("price__lt")
            qs=qs.filter(price__lt=amount)

        if "price__lte" in request.GET:
            amount=request.GET.get("price__lte")
            qs=qs.filter(price__lte=amount)

        if "price__gt" in request.GET:
            amount=request.GET.get("price__gt")
            qs=qs.filter(price__gt=amount)

        if "price__gte" in request.GET:
            amount=request.GET.get("price__gte")
            qs=qs.filter(price__gte=amount)

        return render(request,"book_list.html",{"data":qs})
    

@method_decorator(signin_required,name="dispatch")
class BookDetailView(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)


        return render(request,"book_detail.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Books.objects.get(id=id).delete()

        messages.success(request,"book has been deleted")
        return redirect("book-all")


# book create view
@method_decorator(signin_required,name="dispatch")
class BookCreateView(View):
    def get(self,request,*args,**kwargs):
        form=BookForm()

        return render(request,"book_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):

        form=BookForm(request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"book created successfully")
            return redirect("book-all")
        
        else:
            messages.error(request,"failed to create book")
            return render(request,"book_add.html",{"form":form})
        

# book update view
@method_decorator(signin_required,name="dispatch")
class BookUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookForm(instance=obj)

        return render(request,"book_edit.html",{"form":form})

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookForm(request.POST,instance=obj,files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"book updated successfully")
            return redirect("book-all")
        else:
            messages.error(request,"failed update book")
            return render(request,"book_edit.html",{"form":form})
        

# authentication

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()

        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)

        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"account created successfully")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"failed to create account")
            return render(request,"register.html",{"form":form})
        

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()

        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)

        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                login(request,user_object)
                messages.success(request,f"welcome {request.user}")
                return redirect("book-all")
            messages.error(request,"invalid credential")
            return render(request,"login.html",{"form":form})
        

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    

    
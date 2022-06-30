from django.shortcuts import render,redirect
from django.views.generic import View,RedirectView
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from .models import User,Playlist
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response



class MyView(View):

	def get(self,request):
		if(not request.user.is_authenticated):
			return redirect("myapp:login")
		return render(request,'myapp/index.html')

class MyPlaylistView(View):

    def get(self,request):
        if(not request.user.is_authenticated):
            return redirect("myapp:login")

        return render(request,'myapp/playlist.html',{"movies":Playlist.objects.filter(user=request.user)})



class LoginView(View):
    def get(self,request):
        return render(request,'myapp/login.html',{"form":LoginForm()})
    
    def post(self,request):
        context={}
        error=False
        try:
            form=LoginForm(request.POST)
            if(form.is_valid()):
                phonenumber=form.cleaned_data['phonenumber']
                password=form.cleaned_data['password']
                print(phonenumber,password)
                log=authenticate(request,phonenumber=phonenumber,password=password)
                if(log is not None):
                    login(request,log,backend='django.contrib.auth.backends.ModelBackend')
                    return redirect("myapp:Home")
                else:
                    error="Enter Valid Details.!"
            else:
                try:
                    error=list(form.errors.values())[0][0]
                except:
                    error="Try Again with Valid Details"
            context['form']=form
        except Exception as err:
            error=err
        context['error']=error
        return render(request,'myapp/login.html',context)    




class SignupView(View):

    def get(self,request):
    	return render(request,'myapp/signup.html',{"form":RegisterForm()})
    
    def post(self,request):
        context={}
        error=False
        try:
            form=RegisterForm(request.POST)
            if(form.is_valid()):
                full_name=form.cleaned_data.get('full_name')
                phonenumber=form.cleaned_data.get('phonenumber')
                email=form.cleaned_data.get('email')
                password1=form.cleaned_data.get('password1')
                password2=form.cleaned_data.get('password2')
                if(password1==password2):
                    try:
                        User.objects.create_user(full_name=full_name,phonenumber=phonenumber,email=email,password=password2)
                        return redirect("myapp:login")
                    except:
                        error="Try again with Valid details"
                else:
                    error="Passwords Not Matched"
            else:
                error=list(form.errors.values())[0][0]
            context['form']=form
        except Exception as err:
            error=err
        context['error']=error
        return render(request,'myapp/signup.html',context)


class LogoutView(RedirectView):
    url = '/login/'
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)




class addplaylist_api(APIView):

    @staticmethod
    def get(request):
        img=request.GET.get('image')
        title=request.GET.get('title')
        imdb=request.GET.get('imdb') 
        if(Playlist.objects.filter(title=title,user=request.user).count()==0):
            Playlist.objects.create(user=request.user,title=title,img=img,imdb=imdb)
        return Response({"status":True})

class removeplaylist_api(APIView):

    @staticmethod
    def get(request):
        imdb=request.GET.get('imdb') 
        if(Playlist.objects.filter(imdb=imdb,user=request.user).count()):
            Playlist.objects.filter(imdb=imdb,user=request.user).delete()
        return Response({"status":True})

    
from django.shortcuts import render, redirect, get_object_or_404, reverse

from .models import *
from .forms import *
from .serializers import *

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from django.http import  Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .tasks import create_container, destroy_container

def registerpage(request):
    # checking if the user is already logged or not 
    if not request.user.is_authenticated :
        # creating resgistration form 
        user_form = RegistrationForm()

        if request.method == "POST":
            user_form = RegistrationForm(request.POST)
            if user_form.is_valid():
                # if the form is valid , save the form then create an account for the user and initialize account is locked equal false         
                user = user_form.save()
                account = UserAccount.objects.create(user=user)
                account.save()
                return redirect('login')
        context = {'user_form': user_form}
        return render(request, 'register.html', context)

    else :
        return redirect("landing")

@csrf_exempt
def loginpage(request):
    # checking if the user is already logged or not  
    if not request.user.is_authenticated :

        login_form = LoginForm()
        if request.method == "POST":
            login_form = LoginForm(data=request.POST)
            # checking if the login form is valid or not 
            
            if(login_form.is_valid()):
                # get the data for username and password from the post request then checking if they exists in the database  
                username = request.POST['username']
                password = request.POST["password"]
                user = authenticate(username=username, password=password)

                if user is not None:
                    if (user.is_staff) : # to check first if the user is admin or not 
                        login(request, user)
                        # checking if the next object is have a specific url or not if have we will redirect it 
                        if request.GET.get('next') is not None:
                            return redirect(request.GET.get('next'))
                        else:
                            return redirect('landing')
                    else :
                        # this else if the user isn't an admin or a blocked user 
                        login(request, user)
                        if request.GET.get('next') is not None:
                            return redirect(request.GET.get('next'))
                        else:
                            return redirect('landing')
        context = {"login_form": login_form}
        return render(request, 'login.html', context)
    else :
        return redirect("landing")

def logoutpage(request):
    auth.logout(request)
    return redirect('landing')

def landing(request):
    return render(request, 'landing.html')

class ContainerList(APIView):
    def get(self,request):
        containers = Container.objects.all()
        serializer = ContainersSerializer(containers,many=True)
        return Response(serializer.data)
    
    @csrf_exempt    
    def post(self,request):
        if request.data["process"] == "create":
            postdata = {
                "image_name" : request.data["image_name"],
                "image_tag" : request.data["image_tag"],
                "owner" : request.user.id
            }
            create_container.delay(postdata)
        
        elif request.data["process"] == "destroy":
            postdata = {
                "cont_id" : request.data["cont_id"]
            }
            destroy_container.delay(postdata)
        
            
        serializer = ContainersSerializer(data=postdata)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

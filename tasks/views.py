from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.models import Task
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from tasks.forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
# Create your views here.


@login_required(login_url='login')
def index(request):
    obj = Task.objects.all().filter(user=request.user)
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():

            task = form.save(commit=False)
            task.user=request.user
            task.save()
            return redirect('index')
    context = {
        'object': obj,
        'form': form,
    }
    return render(request, 'task/task_page.html', context)


@login_required(login_url='login')
def updateTask(request,pk):
    task=Task.objects.get(id=pk)
    form=TaskForm(instance=task)
    if request.method=='POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={
        'form':form,
        'task':task
    }
    return render(request,'task/task_update.html',context)

@login_required(login_url='login')
def deleteTask(request,pk):
    task=Task.objects.get(id=pk)
    task.delete()
    return redirect('/')

def registrationPage(request):
    if request.user.is_authenticated:
        # return redirect('/')
        return HttpResponse('Hello')

    else :
        form=CreateUserForm()
        if request.method=='POST':
            form=CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user= form.cleaned_data.get('username')
                messages.success(request,"Everything if Good " +user)
                return redirect(loginPage)
        context = {'form': form}
        return render(request, 'forms/registration.html', context)
            # return HttpResponse('Hello')



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user= authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect(index)
            else :
                messages.info(request,"Username not found")
        context = {}
        return render(request,'forms/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect(loginPage)
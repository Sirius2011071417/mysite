#coding:utf-8
import numpy as np
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from books.handle import handle_uploaded_file
from books.models import MsgBoard
from books.selectAlgo import DataLayer, whichAlgo
from books.forms import RegisterForm, LoginForm, ChangePasswordForm, MsgBoardForm

# Create your views here.
def index(request):
    count = getCount()
    return render(request, 'index.html', {'count':count})

def django(request):
    return render(request, 'django.html')

def login(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password  = data['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.GET:
                    url = request.GET['next']
                else:
                    url = '/'
                return HttpResponseRedirect(url)
                #return render(request, 'index.html', {'user':username})
            else:
                error.append('用户名或密码错误!')
        else:
            error.append('请输入用户名和密码！')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'error':error, 'form':form})

def register(request):
    error = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            password2 = data['password2']
            if not User.objects.filter(username=username):
                if password == password2:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    user = auth.authenticate(username=username, password=password)
                    if user and user.is_active:
                        auth.login(request, user)
                        return HttpResponseRedirect('/')
                       #return render(request, 'index.html', {'user':username})
                else:
                    error.append('前后密码不一致！')
            else:
                error.append('用户名已存在！')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form, 'error':error})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login/')

def changepassword(request, username):
    error = []
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = auth.authenticate(username=username, password=data['oldpassword'])
            if user:
                if data['newpassword'] == data['newpassword1']:
                    newuser = User.objects.get(username__exact=username)
                    newuser.set_password(data['newpassword'])
                    newuser.save()
                    return HttpResponseRedirect('/accounts/login/')
                else:
                    error.append('前后密码不一致!')
            else:
                error.append('请输入正确的旧密码!')
        else:
            error.append('请输入必要的内容!')
    else:
        form = ChangePasswordForm()
    return render(request, 'changepassword.html', {'error':error, 'form':form})

#@login_required
def contact(request):
    if request.method == 'POST':
        form = MsgBoardForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                msg = MsgBoard(username=request.user.username, email=request.user.email, subject=form.cleaned_data['subject'], content=form.cleaned_data['content'])
            else:
                msg = MsgBoard(username=request.META['REMOTE_ADDR'], email=None, subject=form.cleaned_data['subject'], content=form.cleaned_data['content'])
            msg.save()
           # messages.add_message(request, messages.INFO, form.cleaned_data['subject'])
            return HttpResponseRedirect('/contact/success/')
    else:
        form = MsgBoardForm()
    return render(request, 'contact.html', {'form':form})

def contact_success(request):
    return render(request, 'contact_success.html')

def mylist(request, username):
    mylist = MsgBoard.objects.filter(username=username)
    return render(request, 'mylist.html', {'mylist':mylist})
    
def upload(request):
    return render(request, 'algo.html')

def upload_success(request):
    filename = request.FILES["file"]
    handle_uploaded_file(filename)
    return HttpResponse('上传成功!')

def algo(request):
    algoid = request.GET.get('algoid', '')
    algoname = request.GET.get('algoname', '')
    data = DataLayer('t.txt')
    xCnt, dataMat, labelMat, xJson= data.loadDataSet()
    ws, yHat, rssE= whichAlgo(dataMat, labelMat, algoid)
    data = {'xCnt':xCnt, 'dataMat':xJson, 'labelMat':labelMat, 'ws':ws, 'y_predict':yHat, 'rssE':rssE}
    return JsonResponse(data)  
    
def getCount():
    countFile = open('count.dat', 'a+')
    countText = countFile.read()
    try:
        count = int(countText) + 1
    except:
        count = 1
    countFile.seek(0)
    countFile.truncate()
    countFile.write(str(count))
    countFile.flush()
    countFile.close()
    return count

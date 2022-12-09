from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import NewUSerForm
import logging
import boto3
from botocore.exceptions import ClientError
import os
import random
import json
from botocore.config import Config
import printandredirect

def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Lambda block for triggering sns message
            lambdafunctionname = "snstrigger"
            lambdafuninput =  {}
            session = boto3.Session()
            lambda_client = session.client('lambda', region_name='us-east-1')
            response = lambda_client.invoke(FunctionName=lambdafunctionname,
                                        InvocationType='RequestResponse',
                                        Payload=json.dumps(lambdafuninput))
            res_str = response['Payload'].read()
            login(request, user)
            return redirect(printandredirect.signup(user))
    else:
        form = NewUSerForm()
    return render(request, 'accounts/signup.html', { 'form': form })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect(printandredirect.login(user))
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', { 'form': form })

def logout_view(request):
    if request.method == 'POST':
            logout(request)
            return redirect(printandredirect.logout())
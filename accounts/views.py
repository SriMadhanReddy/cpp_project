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

def signup_view(request):
    if request.method == 'POST':
        form = NewUSerForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            print ("sms")
            
            topic_arn = 'arn:aws:sns:us-east-1:219023023686:notifications'
            message = 'Hurray!! we have a new user signed up.'
            subject = 'You Have a new message from SnackPack'
    
            AWS_REGION = 'us-east-1'
            sns_client = boto3.client('sns', region_name=AWS_REGION)
            response = sns_client.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=subject,
                )['MessageId']
            
            login(request, user)
            return redirect('main:home')
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
            return redirect('main:home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', { 'form': form })

def logout_view(request):
    if request.method == 'POST':
            logout(request)
            return redirect('/')
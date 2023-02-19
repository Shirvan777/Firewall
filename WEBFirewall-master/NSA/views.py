from ssl import AlertDescription
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .forms import RulesForm 
from .models import Rules  
import os
import random
import smtplib

'''INDEX SEHIFESI'''
def index(request):
    return render(request, 'index.html')

'''REGISTER SEHIFESI'''
def register(request):
    if request.method == 'POST':
        register.username = request.POST['username']
        register.email = request.POST['email']
        register.password = request.POST['password']
        register.password2 = request.POST['password2']
        
        register.otppp = random.randrange(1000,9999)

        if register.password == register.password2:
            if User.objects.filter(username=register.username).exists():
                messages.info(request, 'Usarname already in use')
                return redirect('register')   
            elif User.objects.filter(email=register.email).exists():
                messages.info(request, 'Email already in use')
                return redirect('register')
            else:
                from email.message import EmailMessage
                import ssl

                # set your email and password
                # please use App Password
                email_address = "your mail"
                email_password = "your password"
                email_receiver = register.email
                # create email
                msg = EmailMessage()
                msg['Subject'] = "NSA App Verification"
                msg['From'] = email_address
                msg['To'] = email_receiver
                msg.set_content('Your verification code is ' + str(register.otppp))

                context = ssl.create_default_context()

                # send email
                with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
                    smtp.login(email_address, email_password)
                    smtp.sendmail(email_address,email_receiver,msg.as_string())
                return redirect('otpp')
        else:
            messages.info(request, 'Passwords must be same') 
        return redirect('register')           
    else:
        return render(request, 'register.html')

def otpp(request):
    if request.method == "POST":
        otp = request.POST['password']
        if int(otp) == register.otppp:
            user = User.objects.create_user(username=register.username,email=register.email,password=register.password)    
            user.save()
            return redirect('login')
        else:
            messages.info(request, 'OTP fail')
    return render(request, 'otp_check.html')


'''LOGIN SEHIFESI'''
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')    
            return redirect('login')
    return render(request, 'login.html')

import win32com.shell.shell as shell

'''HOME SEHIFESI'''
def home(request):
    rules = Rules.objects.all()  
    if request.method == "POST":
        if 'save' in request.POST:
            form = RulesForm(request.POST) 
            if form.is_valid():  
                form.save()
                return redirect('/home')
            else:        
                messages.info(request, 'The rules you added are invalid') 
    form = RulesForm()  
    
    '''BUTTONLARIN IDARESI'''
    if 'start' in request.POST:
        for rule in rules:
            if rule.PROTOCOL_TYPES == 'ICMPv4:8':
                commands = 'netsh advfirewall firewall add rule name="Added rule" protocol=' + rule.PROTOCOL_TYPES + ',any dir=' + rule.DIR + ' action=' + rule.ACTION + ' localip=' + rule.source_ip + ' remoteip=' + rule.dest_ip
                data = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
            elif rule.PROTOCOL_TYPES == 'TCP' or rule.PROTOCOL_TYPES == 'UDP':
                commands = 'netsh advfirewall firewall add rule name="Added rule" protocol=' + rule.PROTOCOL_TYPES + ' dir=' + rule.DIR + ' action=' + rule.ACTION + ' localip=' + rule.source_ip + ' remoteip=' + rule.dest_ip + ' localport=' + str(rule.source_port) + ' remoteport=' + str(rule.dest_port)
                data = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
            else:
                commands = 'netsh advfirewall firewall add rule name="Added rule" protocol=' + rule.PROTOCOL_TYPES + ' dir=' + rule.DIR + ' action=' + rule.ACTION
                data = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
        return render(request,'home.html',{'form':form,'rules':rules,'data':data})
    if 'stop' in request.POST:
        commands = 'netsh advfirewall firewall set rule name="Added rule" new enable=no'
        data = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
        return render(request,'home.html',{'form':form,'rules':rules,'data':data})
    if 'block_a' in request.POST:
        commands = 'netsh advfirewall firewall add rule name="Added rule" dir=in protocol=any action=block'
        data = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
        return render(request,'home.html',{'form':form,'rules':rules,'data':data})
    if 'allow_a' in request.POST:
        commands = 'netsh advfirewall firewall add rule name="Added rule" dir=in protocol=any action=allow'
        data = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
        return render(request,'home.html',{'form':form,'rules':rules,'data':data})        
    if 'block_p' in request.POST:
        commands = 'netsh advfirewall firewall add rule name="Added rule" protocol=icmpv4:8,any dir=in action=block'
        data = shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
        return render(request,'home.html',{'form':form,'rules':rules,'data':data})
    return render(request,'home.html',{'form':form,'rules':rules})

    
'''LOGOUT'''
def logout(request):
    auth.logout(request)
    return redirect('login')

'''RULE-UN SILINMESI'''
def destroy(request, id):  
    rule = Rules.objects.get(id=id)  
    rule.delete()  
    return redirect("/home")  

'''404 SEHIFESI'''
def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})

'''505 SEHIFESI'''
def custom_500_error(request):
    return render(request, "500.html", {})

    
    

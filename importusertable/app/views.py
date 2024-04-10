from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from app.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
# Create your views here.

def registration(request):
    EPFO = ProfileForm()
    EUFO = UserForm()
    d = {'EUFO':EUFO, 'EPFO':EPFO}
    if request.method == 'POST' and request.FILES:
        UFDO = UserForm(request.POST)
        PFDO = ProfileForm(request.POST, request.FILES)
        if UFDO.is_valid():
            MUFDO = UFDO.save(commit=False)
            pw = UFDO.cleaned_data.get('password')
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO = PFDO.save(commit=False)
            MPFDO.username = MUFDO
            MPFDO.save()
            send_mail(
                "Registration",
                "Registration is Successfull",
                "dikshakumari173@gmail.com",
                [MUFDO.email],
                fail_silently=False
            )
            return render(request, 'user_login.html')
        else:
            return HttpResponse('Invalid Data')
    return render(request, 'registration.html',d)

def user_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pw = request.POST.get('pw')
        AUO = authenticate(username=un, password=pw)
        if AUO and AUO.is_active:
            login(request, AUO)
            request.session['username']=un
            return HttpResponseRedirect(reverse('Homepage'))
    return render(request, 'user_login.html')

def index(request):
    if request.session.get('username'):
        un = request.session['username']
        uo = User.objects.get(username=un)
        d = {'uo':uo}
        return render(request, 'home.html', d)
    return render(request, 'home.html')

@login_required
def  user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('Homepage'))


@login_required
def user_profile(request):
    un= request.session.get('username')
    uo=User.objects.get(username=un)
    po=Profile.objects.get(username=uo)
    d={'uo':uo,'po':po}
    return render(request,'user_profile.html',d)


rn=0
def forget_password(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        em=request.POST.get('email')
        UO = User.objects.get(username=un)
        if UO and UO.username==un and UO.email==em:
            global rn
            random_number = random.randint(1000, 9999)
            rn=random_number
            request.session['username']=un
            send_mail(
                "Forget password",
                f"Your verification code is: {random_number}",
                "dikshakumari173@gmail.com",
                [UO.email],
                fail_silently=False
            )
            return render(request, 'otp_verification.html') 
        else:
            return HttpResponse('Username and Email are not matching')
    else:
        return render(request, 'forget_password.html')
    # else:
    #     return HttpResponse('Invalid request method') 



def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if int(otp)==rn:
            return render(request, 'changepassword.html')
            # return render(request, 'changepassword.html') 
        else:
            return HttpResponse('Invalid OTP')
    else:
        return render(request, 'forget_password.html')
    

def changepassword(request):
    if request.method == 'POST':
        CP = request.POST.get('cp')
        un = request.session.get('username')
        IUO = User.objects.get(username=un)
        if IUO:
            IUO.set_password(CP)
            IUO.save()
            return render(request, 'user_login.html')
        return HttpResponse('Invalid')
    


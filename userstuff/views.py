from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
# Create your views here.
################################################################
from userstuff.models import UserProfile


class login(LoginView):
    template_name = 'the_boythesda_user/login.html'
    success_url = '/'

class logout(LogoutView):
    template_name = 'the_boythesda_user/login.html'
    success_url = ''

class passwordReset(PasswordResetView):
    template_name = 'the_boythesda_user/password/passwordReset.html'
    success_url = '/'

class passwordResetDone(PasswordResetDoneView):
    template_name = 'the_boythesda_user/password/passwordResetDone.html'

class passwordResetConfirm(PasswordResetConfirmView):
    template_name = 'the_boythesda_user/password/passwordResetConfirm.html'

class passwordResetComplete(PasswordResetCompleteView):
    template_name = 'the_boythesda_user/password/passwordResetComplete.html'


def userPageView(req, uName):
    user = User.objects.get(username=uName)
    user_additional = UserProfile.objects.get(user = user)
    return render(req, 'the_boythesda_user/userPage.html', context = {'user' : user, 'user_additional' : user_additional})


def register(req):
    form = UserCreationForm(data=req.POST or None)
    if req.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect('userPage/')
    return render(req, 'the_boythesda_user/registration/register.html', {'form' : form})



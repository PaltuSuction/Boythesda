from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response
# Create your views here.
################################################################
from userstuff.forms import UserForm, UserProfileForm
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

@transaction.atomic
def register(req):
    if req.method == 'POST':
        form_user = UserForm(req.POST)
        form_profile = UserProfileForm(data=req.POST, files=req.FILES)
        if form_user.is_valid() and form_profile.is_valid():
            new_user = form_user.save(commit=False)
            new_user.set_password(form_user.cleaned_data['password1'])

            new_user.save()
            #form_profile.save()
            new_user.refresh_from_db()

            username = form_user.cleaned_data['username']
            user = User.objects.get(username=username)
            user.userprofile.user_profile_picture = form_profile.cleaned_data['user_profile_picture']
            user.userprofile.user_email = form_profile.cleaned_data['user_email']
            user.userprofile.save()

            return HttpResponseRedirect('../userID/{}'.format(username))
    else:
        form_user = UserForm()
        form_profile = UserProfileForm()
    return render(req, 'the_boythesda_user/registration/register.html', {'form_user' : form_user, 'form_profile' : form_profile})
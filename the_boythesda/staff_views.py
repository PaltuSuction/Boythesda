from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render, get_object_or_404
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from the_boythesda.forms import UserUpdateForm
from the_boythesda.models import Game, Genre, Publisher, SysReq
from userstuff.forms import UserForm, UserProfileForm


def AllUsersView(req):
    users = User.objects.all().order_by('id')
    current_admin = req.user

    return render(req, 'staff_pages/users/staff_users_page.html', context={'users' : users, 'current_admin' : current_admin,
                                                                           })

def UserUpdateView(req, user_id):
    user = get_object_or_404(User, id = user_id)
    if req.user.id == user.id:
        same_user = True
    else: same_user = False

    if req.method == 'POST':
        form_user = UserUpdateForm(req.POST, instance=user)
        form_profile = UserProfileForm(req.POST, instance=user.userprofile, files=req.FILES)
        if form_user.is_valid():
            if form_profile.is_valid():
                cd = form_profile.cleaned_data
                user.userprofile.user_profile_picture = cd['user_profile_picture']
                form_user.save()
                form_profile.save()
                #return render(req, 'staff_pages/users/staff_users_page.html', context={'form_user': form_user,
                #                                                            'form_profile': form_profile,
                #                                                            'same_user': same_user,
                #                                                            'id_user': user_id, })
                return HttpResponseRedirect('../admin_users_page/')
    else:
        form_user = UserUpdateForm(initial={
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,

        })
        form_profile = UserProfileForm(initial={
            'user_email': user.userprofile.user_email,
            'user_profile_picture': user.userprofile.user_profile_picture,})

    return render(req, 'staff_pages/users/user_update.html', context={'form_user': form_user,
                                                                'form_profile': form_profile,
                                                                'same_user': same_user,
                                                                'id_user': user_id})

def UserDeleteView(req, user_id):
    user = get_object_or_404(User, id = user_id)
    username = user.username
    user.delete()
    return render(req, 'staff_pages/users/user_delete_success.html', context={'username': username})
'''
def AllGamesView(req):
    games = Game.objects.all().order_by('-releaseDate')

    return render(req, 'staff_pages/games/staff_games_page.html', context={'games': games})
'''

class AllGamesView(ListView):
    model = Game
    ordering = ['releaseDate']
    paginate_by = 10
    context_object_name = 'games'
    template_name = 'staff_pages/games/staff_games_page.html'

    def get_context_data(self, **kwargs):
        context = super(AllGamesView, self).get_context_data(**kwargs)
        if not context.get('is_paginated', False):
            return context

        paginator = context.get('paginator')
        num_pages = paginator.num_pages
        current_page = context.get('page_obj')
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context.update({'pages': pages})
        return context

class GameCreateView(CreateView):
    model = Game
    fields = ['title', 'summary', 'genre', 'price', 'scoreCritics', 'scoreUsers', 'publisher', 'Image', 'releaseDate', 'sysReq']
    template_name = 'staff_pages/games/game_create.html'
    success_url = '../admin_users_page/'

class GameUpdateView(UpdateView):
    model = Game
    fields = ['title', 'summary', 'genre', 'price', 'scoreCritics', 'scoreUsers', 'publisher', 'Image', 'releaseDate',
              'sysReq']
    template_name = 'staff_pages/games/game_update.html'
    success_url = '../admin_games_page/'
    context_object_name = 'game'
    #form_class = GameUpdateForm

    def get_initial(self):
        ass = self.object.releaseDate.strftime("%Y-%m-%d")
        a = ass
        return {'title': self.object.title, 'summary': self.object.summary, 'price': self.object.price, 'Image': self.object.Image,
                'scoreCritics': self.object.scoreCritics, 'scoreUsers': self.object.scoreUsers,
                'releaseDate': self.object.releaseDate.strftime("%Y-%m-%d")}

def GameDeleteView(req, game_id):
    game = Game.objects.get(id = game_id)
    game.delete()
    return HttpResponseRedirect('../admin_games_page/')


class GenreCreateView(CreateView):
    model = Genre
    fields = ['name']
    template_name = 'staff_pages/games/genre_create.html'
    success_url = 'gamepage_create/'

class PublisherCreateView(CreateView):
    model = Publisher
    fields = ['name', 'summary', 'foundation_date']
    template_name = 'staff_pages/games/publisher_create.html'
    success_url = 'gamepage_create/'

class PublisherUpdateView(UpdateView):
    model = Publisher
    fields = ['name', 'summary', 'foundation_date']
    template_name = 'staff_pages/games/publisher_update.html'
    success_url = 'gamepage_create/'


class SysReqCreateView(CreateView):
    model = SysReq
    fields = ['configuration_name', 'HDD', 'DDR', 'CPU', 'GPU']
    template_name = 'staff_pages/games/system_req_create.html'
    success_url = 'gamepage_create/'

class SysReqUpdateView(UpdateView):
    model = SysReq
    fields = ['configuration_name', 'HDD', 'DDR', 'CPU', 'GPU']
    template_name = 'staff_pages/games/system_req_update.html'
    success_url = 'gamepage_create/'





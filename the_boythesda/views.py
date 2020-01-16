import math

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, render_to_response, get_object_or_404

# Create your views here.
from django.views import generic
from django.views.generic.edit import FormMixin

from the_boythesda import forms
from the_boythesda.forms import GenreChoiceForm
from the_boythesda.models import Game, Publisher, Genre, SysReq

from userstuff.views import login

from cart.forms import CartAddProductForm

class FormListView(generic.list.ListView, FormMixin):

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class GameListView(FormListView):
    model = Game
    ordering = ['releaseDate', 'scoreUsers']
    template_name = 'mainpage.html'
    paginate_by = 10
    form_class = GenreChoiceForm
    context_object_name = 'game_list'
    #success_url = '/filtered-games'

    def get_context_data(self, **kwargs):
        context = super(GameListView, self).get_context_data(**kwargs)
        context['all_genres'] = Genre.objects.all()
        context['genres_form'] = self.form

        if self.form.is_valid():
            gay = self.form.cleaned_data

            if len(gay['genres']) == 0: context['game_list'] = Game.objects.all()
            else:
                gg = Game.objects.filter(genre__name__contains= list(gay['genres'])[0])
                for i in range(1, len(list(gay['genres']))):
                    gg = gg.filter(genre__name__contains=list(gay['genres'])[i])
                context['game_list'] = gg

        return context


class GameDetailView_2(generic.DetailView):

    model = Game
    template_name = 'individual_pages/games/game.html'
    cart_product_form = CartAddProductForm()

class PublisherListView(generic.ListView):
    model = Publisher
    template_name = 'list_pages/publishers.html'
    paginate_by = 10

class PublisherDetailView(generic.DetailView):
    model = Publisher
    template_name = 'individual_pages/publishers/publisher.html'

def searchGame(req):
    errors = []
    if 'q' in req.GET:
        q = req.GET['q']
        if not q:
            errors.append('Ошибка: пустое поле')
        elif len(q) > 100:
            errors.append('Введите не более 100 символов!')
        else:
            games = Game.objects.filter(title__icontains=q)
            publishers = Publisher.objects.filter(name__contains=q)
            genres = Genre.objects.filter(name__contains=q)
            context = {'games' : games, 'publishers' : publishers, 'genres' : genres, 'query': q}
            return render_to_response('list_pages/games_search_result.html', context)

    return render_to_response('list_pages/games_search_result.html',
                              {'errors': errors})


def GameDetailView(req, pk):
    game = get_object_or_404(Game, pk=pk)
    cart_product_form = CartAddProductForm
    return render(req, 'individual_pages/games/game.html', {'game': game, 'cart_product_form': cart_product_form})

def AboutUs(req):
    return render(req, 'aboutUs.html')

def GamesOfGenre(req, genre_id):
    genre = Genre.objects.get(id = genre_id)
    games_with_genre = Game.objects.filter(genre__name__contains=genre)
    
    return render(req, 'list_pages/gamesWithGenre.html', {'games_with_genres': games_with_genre})

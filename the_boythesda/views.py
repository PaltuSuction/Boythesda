import math

from django.db.models import Q
from django.shortcuts import render, render_to_response, get_object_or_404

# Create your views here.
from django.views import generic

from the_boythesda import forms
from the_boythesda.models import Game, Publisher, Genre, SysReq

from userstuff.views import login

from cart.forms import CartAddProductForm

def AboutUs(req):
    return render(req, 'aboutUs.html')


class GameListView(generic.ListView):
    model = Game
    template_name = 'mainpage.html'

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context['cart_game_form'] = CartAddProductForm()
        return context

    def Search(self):
        queryset = super(GameListView, self).get_queryset()
        q = self.request.GET.get('q')
        if q:
            return queryset.filter(Q(title__contains = q))
        return queryset



class GameDetailView_2(generic.DetailView):

    model = Game
    template_name = 'individual_pages/games/game.html'
    cart_product_form = CartAddProductForm()

class PublisherListView(generic.ListView):
    model = Publisher
    template_name = 'list_pages/publishers.html'

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
            return render_to_response('individual_pages/games/games_search_result.html', context)

    return render_to_response('individual_pages/games/games_search_result.html',
                              {'errors': errors})


def GameDetailView(request, pk):
    game = get_object_or_404(Game, pk=pk)
    cart_product_form = CartAddProductForm
    return render(request, 'individual_pages/games/game.html', {'game': game, 'cart_product_form': cart_product_form})

def GenreListView(req):
    genres = Genre.objects.all()
    context = {'genres' : genres}

    return render_to_response('list_pages/genres.html', context)

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from the_boythesda.models import Game
from .cart import Cart
from .forms import CartAddProductForm

from django.contrib.auth.decorators import login_required
from robokassa.forms import RobokassaForm


@require_POST # Декоратор для разрешения только POST запросов
def cart_add(request, game_pk):
    cart = Cart(request)
    game = get_object_or_404(Game, pk=game_pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(game=game,
                 #quantity=cd['quantity'],
                 quantity=1,
                 update_quantity=cd['update'])
    return redirect('cart_detail')



def cart_remove(request, game_pk):
    cart = Cart(request)
    product = get_object_or_404(Game, pk=game_pk)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


from decimal import Decimal

from boythesda import settings
from the_boythesda.models import Game


class Cart(object):
    def __init__(self, req):
        self.session = req.session
        cart = self.session.get(settings.CART_SESSION_ID) # пытаемся получить корзину с текущей сессии
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, game, quantity = 1, update_quantity = False):
            '''Добавить в корзину игру или изменить количество заказываемых копий'''
            game_pk = str(game.pk)
            if game_pk not in self.cart:
                self.cart[game_pk] = {'quantity': 0, 'price' : str(game.price)}
            if update_quantity:
                self.cart[game_pk]['quantity'] = quantity
            else:
                self.cart[game_pk]['quantity'] += quantity
            self.save()

    def save(self):
            # Обновление сессии cart
            self.session[settings.CART_SESSION_ID] = self.cart
            # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
            self.session.modified = True

    def remove(self, game):
            """
            Удаление товара из корзины.
            """
            game_pk = str(game.pk)
            if game_pk in self.cart:
                del self.cart[game_pk]
                self.save()

    def __iter__(self):
        '''Перебор элементов в корзине и получение игр из базы данных'''

        game_pks = self.cart.keys()
        # получение объектов game и добавление их в корзину
        games = Game.objects.filter(pk__in = game_pks)
        for game in games:
            self.cart[str(game.pk)]['game'] = game

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        '''Подсчет всех товаров в корзине'''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
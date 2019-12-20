from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^add/(?P<game_pk>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<game_pk>\d+)/$', views.cart_remove, name='cart_remove'),

    url(r'^$', views.cart_detail, name='cart_detail'),
]
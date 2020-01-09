from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/$', views.OrderCreate, name='OrderCreate'),

    #url(r'^robokassa/(?P<order_id>\d+)/$', views.pay_with_robokassa, name='Robokassa'),
    url(r'^robokassa/$', views.pay_with_robokassa, name='Robokassa'),
]
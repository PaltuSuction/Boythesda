from django.conf.urls import url
from django.urls import path

from the_boythesda import views


from userstuff import views as userviews

urlpatterns = [
    path('', views.GameListView.as_view(), name = 'main'),

    url(r'^game/(?P<pk>\d+)/$', views.GameDetailView, name = 'game'),

    url(r'^publishers/$', views.PublisherListView.as_view(), name = 'publishers'),

    url(r'^publisher/(?P<pk>\d+)/$', views.PublisherDetailView.as_view(), name = 'publisher'),

    url(r'^about_us/$', views.AboutUs, name = 'about_us'),

    url(r'^genres/$', views.GenreListView, name = 'genres')
]

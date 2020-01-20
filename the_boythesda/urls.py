from django.conf.urls import url
from django.urls import path

from the_boythesda import views, staff_views

from userstuff import views as userviews

urlpatterns = [
    path('', views.GameListView.as_view(), name = 'main'),

    url(r'^game/(?P<pk>\d+)/$', views.GameDetailView, name = 'game'),

    url(r'^publishers/$', views.PublisherListView.as_view(), name = 'publishers'),
    url(r'^publisher/(?P<pk>\d+)/$', views.PublisherDetailView.as_view(), name = 'publisher'),

    url(r'^about_us/$', views.AboutUs, name = 'about_us'),

    url(r'^games_of_genre/(?P<genre_id>\d+)/$', views.GamesOfGenre, name= 'games_of_genre'),

    url(r'^admin_users_page/$', staff_views.AllUsersView, name='admin_users'),
    url(r'^admin_games_page/$', staff_views.AllGamesView.as_view(), name = 'admin_games'),

    url(r'^userpage_update/(?P<user_id>\d+)$', staff_views.UserUpdateView, name='user_update'),
    url(r'^userpage_delete/(?P<user_id>\d+)$', staff_views.UserDeleteView, name = 'user_delete'),

    url(r'^gamepage_create/$', staff_views.GameCreateView.as_view(), name='game_create'),
    url(r'^gamepage_update/(?P<pk>\d+)$', staff_views.GameUpdateView.as_view(), name='game_update'),
    url(r'^gamepage_delete/(?P<game_id>\d+)$', staff_views.GameDeleteView, name='game_delete'),

    url(r'^genre_create/$', staff_views.GenreCreateView.as_view(), name = 'genre_create'),

    url(r'^publisher_create/$', staff_views.PublisherCreateView.as_view(), name = 'publisher_create'),
    url(r'^publisher_update/(?P<pk>\d+)$', staff_views.PublisherUpdateView.as_view(), name = 'publisher_update'),

    url(r'^system_req_create/$', staff_views.SysReqCreateView.as_view(), name = 'system_req_create'),
    url(r'^system_req_update/(?P<pk>\d+)$', staff_views.SysReqUpdateView.as_view(), name = 'system_req_update'),

]

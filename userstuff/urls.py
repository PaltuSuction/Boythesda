from django.conf.urls import url
from django.urls import path

from userstuff import views

urlpatterns = [
    url('login/', views.login.as_view(), name = 'login'),

    url('logout/', views.logout.as_view(), name = 'logout'),

    #path('userID/<str:uName>', views.userPageView, name = 'userPage'),
    url(r'^userID/(?P<uName>\w+)$', views.userPageView, name = 'userPage'),
    path('password-reset/', views.passwordReset.as_view(), name='password_reset'),
    path('password-reset/done/', views.passwordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.passwordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.passwordResetComplete.as_view(), name='password_reset_complete'),

    url(r'^registration/$', views.register, name = 'registration')
]
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup', views.signup, name='signup'),
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('register',views.register, name='register'),
    path('profile',views.profile, name='profile'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('graph',views.graph, name='graph'),
    path('train',views.train, name='train'),
    path('facecam_feed', views.facecam_feed, name='facecam_feed'),
    path('facecam_feed_out', views.facecam_feed_out, name='facecam_feed_out')
]
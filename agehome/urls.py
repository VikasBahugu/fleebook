from django.urls import path, include
from . import views

urlpatterns = [

    path('login', views.loggin, name="login"),
    path('signup', views.signin, name="signup"),

    path('logout', views.logout, name="logout"),


    path('', views.homepage, name='homepage'),
    path('about', views.about, name='about'),
    path('contact/', views.contactusers, name='contact'),
    path('ourfamily', views.ourfamily, name='ourfamily'),

    path('profile', views.profile, name='profile'),

    # For posting a comment
    path('postComment', views.postComment, name='postComment'),

    path('single-standard', views.singlePage, name='single-standard'),
    path('single-standard/<str:title>', views.singlePage, name='single-standards'),

    path('<str:slug>', views.pageNotFound, name='pagenotfound'),


]
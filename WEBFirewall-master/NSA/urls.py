from turtle import home
from unicodedata import name
from django.urls import path
from . import views

'''SEHIFENIN DIRECTORY-LERI'''
urlpatterns =  [
    path('', views.index,name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),   
    path('delete/<int:id>', views.destroy),
    path('otpp',views.otpp,name='otpp')
]

handler404 = 'NSA.views.custom_page_not_found_view'
handler500 = 'NSA.views.custom_500_error'

from django.urls import path
from django.urls.resolvers import URLPattern

from .views import index, login_usuario, votar

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_usuario, name='login_usuario'),
    path('votar/', votar, name='votar')
]

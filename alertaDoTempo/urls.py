from django.urls import path

from . import views

app_name = 'alertaDoTempo'
urlpatterns = [
    path('', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
]
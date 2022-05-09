from django.urls import path

from alertaDoTempo.controllers import ClienteController

app_name = 'alertaDoTempo'
urlpatterns = [
    path('', ClienteController.index, name='index'),
    path('cadastra', ClienteController.cadastra, name='cadastra')
]
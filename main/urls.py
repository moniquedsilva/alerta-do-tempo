"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.urls import path
from main.controllers.ClienteController import ClienteController
from django.conf import settings


urlpatterns = [
    path('cadastrar/', ClienteController.as_view(), name='cadastraIndex'),
    path('cadastrar/insere', ClienteController.cadastra, name='cadastrar'),
    path('cadastrar/loadCidadesByEstado', ClienteController.loadCidadesByEstado, name='loadCidadesByEstado'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


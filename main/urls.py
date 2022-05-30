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

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main.controllers.ClienteController import ClienteController
from main.controllers.HomeController import HomeController
from main.controllers.LoginController import LoginController

urlpatterns = [
    path('', HomeController.as_view(), name='homeIndex'),
    path('cadastrar/', ClienteController.as_view(), name='cadastraIndex'),
    path('cadastrar/insere', ClienteController.as_view(), name='cadastrar'),
    path('cadastrar/loadCidadesByEstado', ClienteController.as_view(), name='loadCidadesByEstado'),
    path('login/', LoginController.as_view(), name='LoginIndex'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

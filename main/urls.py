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
from main.controllers.ClimaController import ClimaController
from main.controllers.DashboardController import DashboardController
from main.controllers.EditarController import EditarController
from main.controllers.HomeController import HomeController
from main.controllers.IndiceUVController import IndiceUVController
from main.controllers.LoginController import LoginController
from main.controllers.OndasController import OndasController

urlpatterns = [
    path('', HomeController.as_view(), name='homeIndex'),
    path('cadastrar/', ClienteController.as_view(), name='cadastraIndex'),
    path('cadastrar/insere', ClienteController.as_view(), name='cadastrar'),
    path('cadastrar/loadCidadesByEstado',
         ClienteController.as_view(), name='loadCidadesByEstado'),
    path('login/', LoginController.as_view(), name='LoginIndex'),
    path('login/user/', LoginController.login_user, name='login'),
    path('logout', LoginController.logout_user, name='logout'),
    path('dashboard', DashboardController.as_view(), name='dashboard'),
    path('clima', ClimaController.as_view(), name='clima'),
    path('indice_uv', IndiceUVController.as_view(), name='indice_uv'),
    path('ondas', OndasController.as_view(), name='ondas'),
    path('dashboard/loadPrevisao',
         DashboardController.as_view(), name='loadPrevisao'),
    path('editar', EditarController.as_view(), name='editarIndex'),
    path('editar/user/', EditarController.editar, name='editar')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler400 = 'main.views.handler400'
handler401 = 'main.views.handler401'
handler403 = 'main.views.handler403'
handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'

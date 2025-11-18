"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from apps.pokemons.views import PokemonViewsSet
from apps.trainers.views import TrainerPokemonViewSet, TrainerViewSet

router = routers.DefaultRouter()
# cria automaticamente toda as URLS para cada View SET
# registra os endpoints seguindo o padrão REST
router.register(r"trainers", TrainerViewSet)
router.register(r"pokemons", PokemonViewsSet)
router.register(r"trainer-pokemons", TrainerPokemonViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1", include(router.urls)),
    # inclui todas as rotas dentro da api/v1
]

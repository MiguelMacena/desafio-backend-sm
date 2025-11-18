from rest_framework import viewsets

from .models import Trainer, TrainerPokemon
from .serializers import TrainerPokemonSerializer, TrainerSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    # representa o conjunto de views para o modelo Trainer
    queryset = Trainer.objects.all()
    # define que todos os objetos serão buscados para CRUD
    serializer_class = TrainerSerializer
    # serializer que será usado para transformar em Json


class TrainerPokemonViewSet(viewsets.ModelViewSet):
    # endpoint de relacionamento TrainerPokemon
    queryset = TrainerPokemon.objects.all()
    # define que todos os objetos serão buscados para CRUD
    serializer_class = TrainerPokemonSerializer
    # serializer que será usado para transformar em Json

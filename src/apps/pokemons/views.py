import requests
from rest_framework import viewsets

from .models import Pokemon
from .serializers import PokemonSerializers


class PokemonViewsSet(viewsets.ModelViewSet):
    # representa o conjunto de views para o modelo Pokemon
    queryset = Pokemon.objects.all()
    # define que todos os objetos serão buscados para CRUD
    serializer_class = PokemonSerializers
    # serializer que será usado para transformar em Json

    def perform_create(self, serializer):
        # sobrescreve o comportamento padrão quando é feito um POST
        nome = self.request.data.get("nome", "").lower()
        # pega os dados recebido do usuário
        # deixa em minúcusculo (Poke API exige tudo em minúsculo)

        poke_url = f"https://pokeapi.co/api/v2/pokemon/{nome}"
        # insere o campo nome no endpoint de listar pokemon

        resp = requests.get(poke_url)
        # busca as informações da Poke API

        if resp.status_code != 200:
            raise ValueError("Pokemon não encontrado na sua Pokedex")

        data = resp.json()
        # armazena tudo sobre o pokemon

        foto = data["sprites"]["front_default"]
        altura = data["height"]
        peso = data["weight"]
        # extração de dados necessários

        serializer.save(
            nome=nome,
            foto=foto,
            altura=altura,
            peso=peso,
        )
        # salva dados necessários no banco

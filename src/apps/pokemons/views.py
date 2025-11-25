import requests
from rest_framework import viewsets
from rest_framework.exceptions import APIException, NotFound

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

        if resp.status_code == 404:
            raise NotFound("Pokemon não encontrado na Pokedex")
        # trata o tipo de erro para ajudar o usuário

        if resp.status_code != 200:
            raise APIException("Erro ao consultar a API")
        # trata o tipo de erro para ajudar o usuário

        data = resp.json()
        # se for da PokeAPI usa sprites
        # se for mock usa foto, altura, peso
        foto = data.get("sprites", {}).get("front_default") or data.get(
            "foto"
        )  # noqa: E501
        altura = data.get("height") or data.get("altura")
        peso = data.get("weight") or data.get("peso")
        # armazena tudo sobre o pokemon

        if not foto or not altura or not peso:
            raise ValueError("Dados do Pokemon inválidos")

        serializer.save(
            nome=nome,
            foto=foto,
            altura=altura,
            peso=peso,
        )
        # salva dados necessários no banco

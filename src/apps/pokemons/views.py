import requests
from rest_framework import generics, viewsets
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response

from apps.core.cache import cache_delete, cache_get, cache_set

from .models import Pokemon
from .serializers import BattleSerializer, PokemonSerializers


class PokemonViewsSet(viewsets.ModelViewSet):
    # representa o conjunto de views para o modelo Pokemon
    queryset = Pokemon.objects.all()
    # define que todos os objetos serão buscados para CRUD
    serializer_class = PokemonSerializers
    # serializer que será usado para transformar em Json

    def list(self, requests, *args, **kwargs):
        key = "pokemon:list"
        # define a chave unica para a lista

        cached = cache_get(key)
        if cached:
            return Response(cached)
        # se a lista já estiver salva no cache não consulta o banco

        response = super().list(requests, *args, **kwargs)
        # caso não esteja faz a consulta no banco

        cache_set(key, response.data)
        # salva no cache

        return response

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

        cache_delete("pokemon:list")
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        # sobrescreve o comportamento padrão quando é feito um UPDATE
        cache_delete("pokemon:list")
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        # sobrescreve o comportamento padrão quando é feito um DELETE
        cache_delete("pokemon:list")
        return super().perform_destroy(instance)


class BattleView(generics.CreateAPIView):
    serializer_class = BattleSerializer

    def perform_create(self, serializer):
        pokemon_1 = serializer.validated_data["pokemon_1"]
        pokemon_2 = serializer.validated_data["pokemon_2"]

        # lógica de batalha
        if pokemon_1.peso > pokemon_2.peso:
            vencedor = pokemon_1.nome
        elif pokemon_2.peso > pokemon_1.peso:
            vencedor = pokemon_2.nome
        else:
            vencedor = "Empate"

        self.resultado = {
            "pokemon_1": pokemon_1.nome,
            "pokemon_2": pokemon_2.nome,
            "vencedor": vencedor,
        }

    def create(self, request, *args, **kwargs):
        return Response(self.resultado)

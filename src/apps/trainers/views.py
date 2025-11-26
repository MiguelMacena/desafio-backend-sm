from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.cache import cache_delete, cache_get, cache_set
from apps.pokemons.models import Pokemon

from .models import Trainer, TrainerPokemon
from .serializers import TrainerPokemonSerializer, TrainerSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    # representa o conjunto de views para o modelo Trainer
    queryset = Trainer.objects.all()
    # define que todos os objetos serão buscados para CRUD
    serializer_class = TrainerSerializer
    # serializer que será usado para transformar em Json

    def list(self, requests, *args, **kwargs):
        key = "trainers:list"
        # define a chave unica para a lista
        cached = cache_get(key)
        if cached:
            return Response(cached)
        # se a lista já estiver salva no cache não consulta db

        response = super().list(requests, *args, **kwargs)
        # caso contrário faz a consulta no db
        cache_set(key, response.data)
        # salva no cache
        return response

    def perform_create(self, serializer):
        # sobrescreve o comportamento padrão quando é feito um POST
        cache_delete("trainers:list")
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        # sobrescreve o comportamento padrão quando é feito um UPDATE
        cache_delete("trainers:list")
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        # sobrescreve o comportamento padrão quando é feito um DELETE
        cache_delete("trainers:list")
        return super().perform_destroy(instance)

    @action(detail=True, methods=["get"])
    # cria uma rota que vai a um id especifico
    def pokemons(self, request, pk=None):
        trainer = self.get_object()
        # pega o treiner que corresponde ao pk

        key = f"trainer:{trainer.id}:pokemons"
        # define key que terá o trainer.id
        cached = cache_get(key)
        if cached:
            return Response(cached)
        # se a lista já estiver salva no cache não consulta db

        queryset = TrainerPokemon.objects.filter(trainer=trainer)
        serializer = TrainerPokemonSerializer(queryset, many=True)

        cache_set(key, serializer.data)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    # cria uma rota extra que vai a um id especifico
    def add_pokemon(self, request, pk=None):
        trainer = self.get_object()
        # pega o treiner que corresponde ao pk

        pokemon_id = request.data.get("pokemon_id")
        if not pokemon_id:
            return Response({"error": "pokemon_id é obrigatório"}, status=400)
        # pega o id do pokemon e força a obrigatoriedade, caso contrário 400

        try:
            pokemon = Pokemon.objects.get(id=pokemon_id)
        except Pokemon.DoesNotExist:
            return Response({"error": "Pokemon não encontrado"}, status=404)
        # tenta buscar o Pokemon pelo ID informado, caso contrário 404

        if TrainerPokemon.objects.filter(
            trainer=trainer, pokemon=pokemon
        ).exists():  # noqa: E501
            return Response(
                {"error": "Este pokemon já está associado ao treinador"},
                status=400,
            )
        # valida se já existe um relacionamento
        #  entre o pokemon e o treinador

        TrainerPokemon.objects.create(trainer=trainer, pokemon=pokemon)
        # cria a linha de relação
        # entre Pokemon e Treiner na TrainerPokemon

        # Invalida o cache correto
        cache_delete(f"trainer:{trainer.id}:pokemons")

        return Response(
            {
                "message": f"Pokemon '{pokemon.nome}' adicionado ao treinador {trainer.nome}"  # noqa: E501
            },
            status=201,
        )

    @action(
        detail=True,
        methods=["delete"],
        url_path="remove-pokemon/(?P<pokemon_id>[^/.]+)",
    )
    # especifica que a rota depende de um id do treinador
    # define um padrão dinâmico dentro da URL
    def remove_pokemon(self, request, pk=None, pokemon_id=None):
        trainer = self.get_object()
        # pega o treiner que corresponde ao pk
        try:
            pokemon = Pokemon.objects.get(id=pokemon_id)
        except Pokemon.DoesNotExist:
            return Response({"error": "Pokemon não encontrado. "}, status=404)
        # verifica se o pokemon existe

        try:
            relation = TrainerPokemon.objects.get(
                trainer=trainer, pokemon=pokemon
            )  # noqa: E501
            relation.delete()
        except TrainerPokemon.DoesNotExist:
            return Response(
                {"error": "Este treinador não possui este Pokemon"}, status=404
            )
        # busca a relação entre o pokemon e o treinador

        return Response(
            {"message": "Pokemon removido com sucesso"}, status=200
        )  # noqa: E501
        # se existir apaga


class TrainerPokemonViewSet(viewsets.ModelViewSet):
    queryset = TrainerPokemon.objects.all()
    serializer_class = TrainerPokemonSerializer

    def get_queryset(self):
        queryset = TrainerPokemon.objects.all()
        trainer_id = self.request.query_params.get("trainer_id")

        if trainer_id:
            queryset = queryset.filter(trainer_id=trainer_id)

        return queryset

    def perform_create(self, serializer):
        # sobrescreve o comportamento padrão quando é feito um POST
        instance = serializer.save()
        trainer_id = instance.trainer.id
        cache_delete(f"trainer:{trainer_id}:pokemons")

    def perform_update(self, serializer):
        # sobrescreve o comportamento padrão quando é feito um UPDATE
        instance = serializer.save()
        trainer_id = instance.trainer.id
        cache_delete(f"trainer:{trainer_id}:pokemons")
        return instance

    def perform_destroy(self, instance):
        # sobrescreve o comportamento padrão quando é feito um DELETE
        trainer_id = instance.trainer.id
        cache_delete(f"trainer:{trainer_id}:pokemons")
        return super().perform_destroy(instance)

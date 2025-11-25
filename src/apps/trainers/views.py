from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.pokemons.models import Pokemon

from .models import Trainer, TrainerPokemon
from .serializers import TrainerPokemonSerializer, TrainerSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    # representa o conjunto de views para o modelo Trainer
    queryset = Trainer.objects.all()
    # define que todos os objetos serão buscados para CRUD
    serializer_class = TrainerSerializer
    # serializer que será usado para transformar em Json

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
            # valida se já existe um relacionamento
            #  entre o pokemon e o treinador
            return Response(
                {"error": "Este pokemon já está associado ao treinador"},
                status=400,
            )

        TrainerPokemon.objects.create(trainer=trainer, pokemon=pokemon)
        # cria a linha de relação
        # entre Pokemon e Treiner na TrainerPokemon

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
            return Response(
                {"error": "Pokemon não encontrado. "}, status=404
            )  # noqa: E501
        # verifica se o pokemon existe

        try:
            relation = TrainerPokemon.objects.get(
                trainer=trainer, pokemon=pokemon
            )  # noqa: E501
            relation.delete()
        except TrainerPokemon.DoesNotExist:
            return Response(
                {"error": "Este treinador não possui este Pokemon"}, status=404
            )  # noqa: E501
        # busca a relação entre o pokemon e o treinador

        return Response(
            {"message": "Pokemon removido com sucesso"}, status=200
        )  # noqa: E501
        # se existir apaga


class TrainerPokemonViewSet(viewsets.ModelViewSet):
    # endpoint de relacionamento TrainerPokemon
    queryset = TrainerPokemon.objects.all()
    # define que todos os objetos serão buscados para CRUD
    serializer_class = TrainerPokemonSerializer
    # serializer que será usado para transformar em Json

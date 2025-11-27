from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pokemons.models import Pokemon
from apps.trainers.models import TrainerPokemon

from .serializers import BattleSerializer


class BattleView(APIView):

    def post(self, request):

        serializer = BattleSerializer(data=request.data)

        if serializer.is_valid():

            id1 = request.data.get("pokemon_1")
            id2 = request.data.get("pokemon_2")
            # pega o corpo da requisição
            # e os dois id's dos pokemons

            if not id1 or not id2:
                return Response(
                    {"error": "pokemon_1 e pokemon_2 são obrigatórios"},
                    status=400,  # noqa: E501
                )
            # checa se algum dos id's não foi enviado
            try:
                p1 = Pokemon.objects.get(id=id1)
                p2 = Pokemon.objects.get(id=id2)
            except Pokemon.DoesNotExist:
                return Response(
                    {"error": "Pokemon não encontrado"}, status=404
                )  # noqa: E501
            # busca no db os pokemons com os id's

            t1 = TrainerPokemon.objects.filter(pokemon=p1).first()
            t2 = TrainerPokemon.objects.filter(pokemon=p2).first()
            # busca a qual trainer o pokemon está associado

            if t1 and t2 and t1.trainer.id == t2.trainer.id:
                return Response(
                    {"error": "Pokemons são do mesmo treinador"}, status=400
                )  # noqa: E501
            # valida se treinadores existem e se os id's são os mesmos

            # valida peso para definir vencedor da batalha
            if p1.peso > p2.peso:
                winner = p1.nome
            elif p2.peso > p1.peso:
                winner = p2.nome
            else:
                return Response(
                    {
                        "resultado": "empate",
                        "detalhes": "Mesma quantidade de peso",
                    }  # noqa: E501
                )

        return Response({"resultado": "vencedor", "pokemon": winner})

    def get(self, request):
        trainer_pokemon = TrainerPokemon.objects.select_related(
            "trainer", "pokemon"
        )  # noqa: E501

        trainers_data = []
        treinadores_map = {}

        for tp in trainer_pokemon:
            trainer_id = tp.trainer.id

            if trainer_id not in treinadores_map:
                treinadores_map[trainer_id] = {
                    "trainer_id": trainer_id,
                    "trainer_nome": tp.trainer.nome,
                    "pokemon": [],
                }

            treinadores_map[trainer_id]["pokemon"].append(
                {
                    "id": tp.pokemon.id,
                    "nome": tp.pokemon.nome,
                    "peso": tp.pokemon.peso,
                }  # noqa: E501
            )

        trainers_data = list(treinadores_map.values())

        pokemons_data = [
            {
                "id": tp.pokemon.id,
                "nome": tp.pokemon.nome,
                "treinador": tp.trainer.nome,
            }  # noqa: E501
            for tp in trainer_pokemon
        ]

        return Response(
            {
                "pokemons_disponiveis": pokemons_data,
                "treinadores": trainers_data,
            }  # noqa: E501
        )

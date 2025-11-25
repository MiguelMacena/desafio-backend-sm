from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pokemons.models import Pokemon
from apps.trainers.models import TrainerPokemon


class BattleView(APIView):

    def post(self, request):
        id1 = request.data.get("pokemon_1")
        id2 = request.data.get("pokemon_2")
        # pega o corpo da requisição
        # e os dois id's dos pokemons

        if not id1 or not id2:
            return Response(
                {"error": "pokemon_1 e pokemon_2 são obrigatórios"}, status=400
            )
        # checa se algum dos id's não foi enviado
        try:
            p1 = Pokemon.objects.get(id=id1)
            p2 = Pokemon.objects.get(id=id2)
        except Pokemon.DoesNotExist:
            return Response({"error": "Pokemon não encontrado"}, status=404)
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
                {"resultado": "empate", "detalhes": "Mesma quantidade de peso"}
            )

        return Response({"resultado": "vencedor", "pokemon": winner})

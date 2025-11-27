from rest_framework import serializers

from .models import Pokemon


class PokemonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        # mapeia os tipos de campo e converte o model para Json
        fields = [
            "id",
            "nome",
            "foto",
            "altura",
            "peso",
            "criado_em",
            "atualizado_em",
        ]
        # define quais campso do model serão expostos na API

        read_only_fields = ("foto", "altura", "peso")
        # garante que o usuário só envie o nome


class BattleSerializer(serializers.Serializer):
    pokemon_1 = serializers.IntegerField()
    pokemon_2 = serializers.IntegerField()

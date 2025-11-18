from rest_framework import serializers

from .models import Trainer, TrainerPokemon


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        # mapeia os tipos de campo e converte o model para Json
        fields = ["id", "nome", "idade", "criado_em", "atualizado_em"]
        # define quais campso do model serão expostos na API


class TrainerPokemonSerializer(serializers.ModelSerializer):
    trainer_nome = serializers.CharField(source="trainer.nome", read_only=True)
    # cria um campo novo que não existe no model e pega o valor de trainer.nome
    pokemon_nome = serializers.CharField(source="pokemon.nome", read_only=True)
    # cria um campo novo que não existe no model e pega o valor de pokemon.nome

    class Meta:
        model = TrainerPokemon
        # informa qual modelo deve transformar em Json
        fields = ["id", "trainer", "trainer_nome", "pokemon", "pokemon_nome"]
        # define quais campos aparecem no Json retornado pela API

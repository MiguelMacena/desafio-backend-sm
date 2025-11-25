import pytest

from apps.pokemons.models import Pokemon
from apps.trainers.models import Trainer, TrainerPokemon


@pytest.mark.django_db
def test_battle_pokemon_1_wins(client):
    trainer1 = Trainer.objects.create(nome="Ash", idade=15)
    # cria o trainer ficticio

    p1 = Pokemon.objects.create(nome="pikachu", peso=50)
    p2 = Pokemon.objects.create(nome="bulbasaur", peso=20)
    # cria os pokemons ficticios

    TrainerPokemon.objects.create(trainer=trainer1, pokemon=p1)
    TrainerPokemon.objects.create(trainer=trainer1, pokemon=p2)
    # cria o relacionamento entre pokemon e treinador
    # atrela os dois pokemons ao mesmo treinador

    response = client.post(
        "/api/v1/battle/", {"pokemon_1": p1.id, "pokemon_2": p2.id}
    )  # noqa: E501

    assert response.status_code == 400
    #  valida se foi dado 400
    # os pokemons são do mesmo treinador


@pytest.mark.django_db
def test_battle_victory(client):
    t1 = Trainer.objects.create(nome="Ash", idade=15)
    t2 = Trainer.objects.create(nome="Gary", idade=16)
    # cria o trainer ficticio

    p1 = Pokemon.objects.create(nome="pikachu", peso=100)
    p2 = Pokemon.objects.create(nome="charmander", peso=50)
    # cria os pokemons ficticios

    TrainerPokemon.objects.create(trainer=t1, pokemon=p1)
    TrainerPokemon.objects.create(trainer=t2, pokemon=p2)
    # cria o relacionamento entre pokemon e treinador
    # atrela os dois pokemons a treinadores distintos

    response = client.post(
        "/api/v1/battle/", {"pokemon_1": p1.id, "pokemon_2": p2.id}
    )  # noqa: E501

    assert response.status_code == 200
    assert response.data["pokemon"] == "pikachu"
    # valida se deu 200
    # pokemon vencedor deve ser o pikachu

import pytest
from django.core.cache import cache
from apps.trainers.models import Trainer, TrainerPokemon
from apps.pokemons.models import Pokemon


@pytest.mark.django_db
def test_cache_invalidation_trainer_pokemon(client):
    cache.clear()

    trainer = Trainer.objects.create(nome="Ash", idade=15)
    # cria o treinador

    p1 = Pokemon.objects.create(
        nome="pikachu",
        altura=4,
        peso=40,
        foto="url",
    )
    p2 = Pokemon.objects.create(nome="bulbasaur", altura=7, peso=60, foto="url")
    # cria o pokemon

    TrainerPokemon.objects.create(trainer=trainer, pokemon=p1)
    # cria uma relaçao entre o treinador e o pokemon 1

    response1 = client.get(f"/api/v1/trainers/{trainer.id}/pokemons/")
    assert len(response1.json()) == 1
    # realiza um GET dos pokemons que possui relação
    # com o treinador

    client.post(
        f"/api/v1/trainers/{trainer.id}/add_pokemon/",
        {"pokemon_id": p2.id},
        content_type="application/json",
    )
    # adiciona o segundo pokemon via endpoint

    response2 = client.get(f"/api/v1/trainers/{trainer.id}/pokemons/")
    assert len(response2.json()) == 2

    cache.clear()

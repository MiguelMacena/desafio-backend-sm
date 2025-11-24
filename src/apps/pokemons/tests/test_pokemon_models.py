import pytest

from apps.pokemons.models import Pokemon


@pytest.mark.django_db
def test_pokemon_model_str():
    # teste model pokemon
    poke = Pokemon.objects.create(nome="pikachu")
    # cria um pokemon de nome Pikachu
    assert str(poke) == "pikachu"
    # valida se existe um Pokemon no str que bate com as inf

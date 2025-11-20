import pytest

from apps.pokemons.models import Pokemon
from apps.trainers.models import Trainer, TrainerPokemon


@pytest.mark.django_db
# permite o uso do db
def test_trainer_model_str():
    # teste model trainer
    trainer = Trainer.objects.create(nome="Ash", idade=15)
    # cria um treiner de nome Ash e idade 15
    assert str(trainer) == "Ash"
    # valida se existe um treiner no str que bate com as inf


@pytest.mark.django_db
# permite o uso do db
def test_trainerpokemon_unique_constraint():
    # testa a relação entre treinador e pokemon
    trainer = Trainer.objects.create(nome="Ash", idade=15)
    # faz a criação do trainer
    pokemon = Pokemon.objects.create(nome="pikachu")
    # faz a criação do pokemon

    TrainerPokemon.objects.create(trainer=trainer, pokemon=pokemon)
    # cria um relacionamento válido - Ash possui Pikachu

    with pytest.raises(Exception):
        TrainerPokemon.objects.create(trainer=trainer, pokemon=pokemon)
        # Exception é lançada se o mesmo
        # treinador ter mesmo pokemon 2 vezes

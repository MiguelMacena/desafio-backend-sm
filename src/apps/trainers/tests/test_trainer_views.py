import pytest

from apps.pokemons.models import Pokemon
from apps.trainers.models import Trainer, TrainerPokemon


@pytest.mark.django_db
def test_create_trainer_api(client):
    # cria POST do treiner
    url = "/api/v1/trainers/"
    payload = {"nome": "Ash", "idade": 15}
    # passa os dados

    response = client.post(url, payload)
    # simula um cliente real fazendo requisições

    assert response.status_code == 201
    # confirma se deu 201 Created
    assert Trainer.objects.count() == 1
    # Confirma se tem 1 treinador no db
    assert response.data["nome"] == "Ash"
    # confirma se o nome da requisição
    # feita pelo cliente bate com o db


@pytest.mark.django_db
def test_list_trainers_api(client):
    # cria GET do treiner
    Trainer.objects.create(nome="Ash", idade=15)
    Trainer.objects.create(nome="Misty", idade=14)
    # passa os dados

    response = client.get("/api/v1/trainers/")
    # lista os dados na URL

    assert response.status_code == 200
    # confirma se deu 200
    assert len(response.data) == 2
    # confirma se foi listado
    # dois treinadores


@pytest.mark.django_db
def test_add_pokemon_to_trainer(client):
    trainer = Trainer.objects.create(nome="Ash", idade=15)
    pokemon = Pokemon.objects.create(nome="pikachu")
    # cria treinador e pokemon ficticio

    url = f"/api/v1/trainers/{trainer.id}/add-pokemon/"
    payload = {"pokemon_id": pokemon.id}
    # indica qual o enpoint do método add_pokemon

    response = client.post(url, payload, format="json")
    # simula um POST enviando o pokemon_id

    assert response.status_code == 201
    # valida se foi CREATED
    assert TrainerPokemon.objects.count() == 1
    # garante que foi feito a criação da relação
    # na tabela


@pytest.mark.django_db
def test_remove_pokemon_from_trainer(client):
    trainer = Trainer.objects.create(nome="Ash", idade=15)
    pokemon = Pokemon.objects.create(nome="pikachu")
    TrainerPokemon.objects.create(trainer=trainer, pokemon=pokemon)
    # cria treinador, pokemon e relação ficticia

    url = f"/api/v1/trainers/{trainer.id}/remove-pokemon/{pokemon.id}/"
    # passa a base da URL para o DELETE

    response = client.delete(url, format="json")
    # simula um DELETE enviando o pokemon_id

    assert response.status_code == 200
    # valida se deu SUCESS
    assert TrainerPokemon.objects.count() == 0
    # garante que foi feito a remoção da table

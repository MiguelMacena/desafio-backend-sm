import pytest

from apps.pokemons.models import Pokemon
from apps.trainers.models import Trainer, TrainerPokemon


class FakePokeResponse:
    # objeto falso que simula resposta da PokeAPI
    status_code = 200

    def json(self):
        return {
            "sprites": {"front_default": "foto_url"},
            "height": 10,
            "weight": 100,
        }


@pytest.mark.django_db
def test_create_pokemon_with_pokeapi(client, monkeypatch):
    def fake_get(url):
        # substitui a função requests.get
        return FakePokeResponse()

    monkeypatch.setattr("apps.pokemons.views.requests.get", fake_get)
    # chama o fake_get e retorna o FakePokeResponse
    # substitui dentro do apps.pokemons.views

    payload = {"nome": "pikachu"}

    response = client.post("/api/v1/pokemons/", payload)
    # simula um POST na criação do pokemon

    assert response.status_code == 201
    # valida se retornou como Created
    data = response.data

    assert data["nome"] == "pikachu"
    assert data["foto"] == "foto_url"
    assert data["altura"] == 10
    assert data["peso"] == 100

    # realiza asserções para os valores aparecem
    # exatamente igual o FakePokeResponse


@pytest.mark.django_db
def test_create_pokemon_api_error(client, monkeypatch):
    class FakeErrorResp:
        status_code = 404

    # cria uma classe simples retornando um obj com 404

    def fake_get(url):
        return FakeErrorResp()

    monkeypatch.setattr("apps.pokemons.views.requests.get", fake_get)
    # chama o fake_get e retorna o FakePokeResponse
    # substitui dentro do apps.pokemons.views

    payload = {"nome": "xyza1222"}

    response = client.post("/api/v1/pokemons/", payload)
    # simula um POST na criação do pokemon
    assert response.status_code == 404
    # valida que o erro deve retornar como 404
    # quando a API falhar


@pytest.mark.django_db
def test_create_trainerpokemon_api(client):
    trainer = Trainer.objects.create(nome="Ash", idade=15)
    pokemon = Pokemon.objects.create(nome="pikachu")
    # criação de objetos necessários
    # um treinador e um pokmemon existente

    payload = {"trainer": trainer.id, "pokemon": pokemon.id}
    # monta o payload do post com base no id

    response = client.post("/api/v1/trainer-pokemons/", payload)

    assert response.status_code == 201
    # valida se retornou Created
    assert TrainerPokemon.objects.count() == 1
    # garante se mais um objeto foi criado no db

import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.django_db
@patch("apps.pokemons.views.requests.get")
def test_full_flow_integration(mock_requests, client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "nome":"pikachu",
        "foto":"https://pokeapi.co/media/pikachu.png",
        "altura": 4,
        "peso": 60,
    }  

    mock_requests.return_value = mock_response

    t1 = client.post("/api/v1/trainers/", 
                     {"nome":"Ash",
                        "idade": 15,
    }).json()

    t2 = client.post("/api/v1/trainers/",
                     {"nome": "Gary", 
                      "idade":16,
    }).json()
    # cria treinadores

    p1 = client.post("/api/v1/pokemons/",{"nome":"pikachu"}).json()
    # cria pokemon 1  via API

    mock_response.json.return_value = {
        "nome":"charmader",
        "foto": "https://pokeapi.co/media/charmander.png",
        "altura": 6,
        "peso":40,
    }
     
    p2 = client.post("/api/v1/pokemons/",{"nome":"charmander"}).json()
    # altera para pokemon 2 - Mock e API


    client.post(f"/api/v1/trainers/{t1["id"]}/add_pokemon/",{
        "pokemon_id": p1["id"]
    })

    client.post(f"/api/v1/trainers/{t2["id"]}/add_pokemon", {
        "pokemon_id": p2["id"]
    })
    # associa pokemons

    reponse = client.post("/api/v1/battle/",
                           {"pokemon_1": p1["id"],
                            "pokemon_2": p2["id"]
                            })
    # testa batalha

    data = reponse.json()

    assert reponse.status_code == 200
    assert data["resultado"] == "vencedor"
    assert data ["pokemon"] == "pikachu"
    # valida se deu Sucesso
    # confirma se houve vencedor
    # confirma se o vencedor é o pikachu
    
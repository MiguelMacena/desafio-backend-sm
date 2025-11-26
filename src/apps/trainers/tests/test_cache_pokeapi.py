from unittest.mock import patch

import pytest
from django.core.cache import cache

from apps.pokemons.services.pokeapi import fetch_pokemon_data


@pytest.mark.django_db
@patch("apps.pokemons.services.pokeapi.requests.get")
def test_pokeapi_uses_cache(mock_get):
    # limpa cache para proximos testes
    cache.clear()

    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "name": "pikachu",
        "sprites": {"front_default": "url"},
        "height": 4,
        "weight": 40,
    }
    # cria o pokemon via Mock

    data1 = fetch_pokemon_data("pikachu")
    assert mock_get.call_count == 1
    # verifica se houve uma chamada real na API

    data2 = fetch_pokemon_data("pikachu")
    assert mock_get.call_count == 1
    assert data1 == data2
    # o mesmo fecth que deve ser puxado do cache
    # nao deve ser chamado na API
    # valida se os dados do data1 e data2 são iguais

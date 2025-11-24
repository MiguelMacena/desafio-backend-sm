from apps.pokemons.serializers import PokemonSerializers


def test_pokemon_serializer_field():
    # testa o serializer do Pokemon
    serializer = PokemonSerializers()
    # serializer é todos os fields registrados
    # dentro do PokemonSerializers
    expected = {
        "id",
        "nome",
        "foto",
        "altura",
        "peso",
        "criado_em",
        "atualizado_em",
    }
    # padrão esperado
    assert set(serializer.fields.keys()) == expected
    # valida se o padrão está de acordo com o esperado

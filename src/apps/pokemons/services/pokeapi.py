import requests

from apps.core.cache import cache_get, cache_set


def fetch_pokemon_data(nome):
    key = f"pokeapi:{nome}"
    # cria uma chave única para cada Pokemon

    cached = cache_get(key)
    if cached:
        return cached
    # se o Pokemon já estiver no cache ele retorna sem chamar API externa

    response = requests.get(
        f"https://pokeapi.co/api/v2/pokemon/{nome.lower()}/"
    )  # noqa: E501

    # faz a chamada na API caso não esteja no cache

    if response.status_code != 200:
        raise ValueError("Pokemon não encontrado na PokeAPI")

    # caso o pokemon não exista é lançado o erro

    data = response.json()

    result = {
        "nome": data["name"],
        "foto": data["sprites"]["front_default"],
        "altura": data["height"],
        "peso": data["weight"],
    }
    # formata somente os dados necessários

    cache_set(key, result)
    # salva no cache

    return result

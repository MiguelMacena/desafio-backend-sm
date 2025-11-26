import pytest
from django.core.cache import cache
from apps.trainers.models import Trainer


@pytest.mark.django_db
def test_list_trainers_cached(client):
    # limpa cache para proximos testes
    cache.clear()

    Trainer.objects.create(nome="Ash", idade=15)
    Trainer.objects.create(nome="Misty", idade=14)
    # cria os treinadores

    response1 = client.get("/api/v1/trainers/")
    assert response1.status_code == 200
    assert len(response1.json()) == 2
    # lista treinadores e obj criados

    Trainer.objects.create(nome="Brock", idade=17)
    # cria um treinador sem fazer o POST

    response2 = client.get("/api/v1/trainers/")
    assert len(response2.json()) == 2
    # dá um GET que deve exibir somente
    # 2 treinadores

    cache.clear()

import pytest
from django.urls import reverse
from apps.trainers.models import Trainer

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
    Trainer.objects.create(nome="Ash", idade =15)
    Trainer.objects.create(nome = "Misty", idade =14)
    # passa os dados

    response = client.get("/api/v1/trainers/")
    # lista os dados na URL

    assert response.status_code == 200
    # confirma se deu 200
    assert len(response.data) ==2
    # confirma se foi listado 
    # dois treinadores
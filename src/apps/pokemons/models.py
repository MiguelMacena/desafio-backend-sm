from django.db import models


class Pokemon(models.Model):
    # representa o modelo de um Pokemon

    nome = models.CharField(max_length=100, unique=True)
    # dois pokemons não podem ter o mesmo nome

    # dados que serão preenchidos pela PokeAPI

    foto = models.URLField(null=True, blank=True)
    altura = models.PositiveIntegerField(null=True, blank=True)
    peso = models.PositiveIntegerField(null=True, blank=True)
    # URLField valida se o texto tem formato de URL
    # null e blank True porque quem preenche é a POKE API

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

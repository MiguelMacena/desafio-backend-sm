from django.db import models

from apps.pokemons.models import Pokemon


class Trainer(models.Model):
    # representa o modelo de um treinador

    nome = models.CharField(max_length=100)
    idade = models.PositiveBigIntegerField()

    pokemon = models.ManyToManyField(
        # cria relacionamento ManyToMany entre treinador e Pokemons
        "Pokemon",
        through="TrainerPokemon",
        # possibilita controlar a tabela criada pelo Django
        related_name="treinadores",
        # define como acessar os treinadores a partir de um Pokemon
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class TrainerPokemon(models.Model):

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    # cria uma relação entre treinador e pokemom
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    # cria uma relação dentre pokemon e treinador

    class Meta:
        unique_together = ("trainer", "pokemon")
        # barra a possibilidade de 1 treinador ter o mesmo pokemon

    def __str__(self):
        return f"{self.trainer.nome} possui {self.pokemon.nome}"

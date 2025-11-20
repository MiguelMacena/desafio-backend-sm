from apps.trainers.serializers import TrainerSerializer


def test_trainer_serializer_fields():
    serializer = TrainerSerializer()
    expected = {"id", "nome", "idade", "criado_em", "atualizado_em"}
    assert set(serializer.fields.keys()) == expected

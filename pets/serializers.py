from rest_framework import serializers
from groups.serialisers import GroupSerializer
from traits.serializers import TraitSerializer
from .models import Choices


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Choices.choices, default=Choices.DEFAULT)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

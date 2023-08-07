from rest_framework import serializers
from groups.serialisers import GroupSerializer
from traits.serializers import TraitSerializer


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.CharField(max_length=20)
    group = GroupSerializer()
    traits = TraitSerializer(many=True)

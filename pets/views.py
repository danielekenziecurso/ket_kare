from django.shortcuts import get_object_or_404
from rest_framework.views import status, Request, Response, APIView
from .models import Pet
from groups.models import Group
from traits.models import Trait
from .serializers import PetSerializer
from rest_framework.pagination import PageNumberPagination


class PetView(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receive_group = serializer.validated_data.pop("group")
        receive_traits = serializer.validated_data.pop("traits")
        group = Group.objects.filter(
            scientific_name__iexact=receive_group["scientific_name"]
        ).first()
        if not group:
            group = Group.objects.create(**receive_group)
        pet = Pet.objects.create(**serializer.validated_data, group=group)
        for traits in receive_traits:
            trait = Trait.objects.filter(name__iexact=traits["name"]).first()
            if not trait:
                trait = Trait.objects.create(**traits)

            pet.traits.add(trait)

        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        traits = request.query_params.get("trait")

        if traits:
            pets = Pet.objects.filter(traits__name=traits).all()
        else:
            pets = Pet.objects.all()
        result = self.paginate_queryset(pets, request)
        serializer = PetSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class PetDetailVieaw(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)

        serializer = PetSerializer(pet)

        return Response(serializer.data)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)
        serializer = PetSerializer(instance=pet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        receive_group = serializer.validated_data.pop("group", None)
        receive_traits = serializer.validated_data.pop("traits", None)
        if receive_group:
            group = Group.objects.filter(
                scientific_name__iexact=receive_group["scientific_name"]
            ).first()
            if not group:
                group = Group.objects.create(**receive_group)
            pet.group = group
        if receive_traits:
            traits_to_add = []
            for trait_data in receive_traits:
                trait = Trait.objects.filter(name__iexact=trait_data["name"]).first()
                if not trait:
                    trait = Trait.objects.create(**trait_data)
                traits_to_add.append(trait)
            pet.traits.set(traits_to_add)
        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)
        pet.save()
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, pk=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        # pet = None
        if not group:
            group = Group.objects.create(**receive_group)
            pet = Pet.objects.create(**serializer.validated_data, group=group)
        for traits in receive_traits:
            trait = Trait.objects.filter(name__iexact=traits["name"]).first()
            if not trait:
                trait = Trait.objects.create(**traits)
            pet.traits.add(trait)

        pet.traits.add(trait)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        traits = request.query_params.get("trait")
        pets = Pet.objects.all()
        if traits:
            filtered_traits = Pet.objects.filter(trait_name=traits).all()
            result = self.paginate_queryset(filtered_traits, request)
        else:
            result = self.paginate_queryset(pets, request)
        serializer = PetSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)

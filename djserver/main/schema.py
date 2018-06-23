import graphene

from graphene_django.types import DjangoObjectType

from main.models import City, State


class StateType(DjangoObjectType):
    class Meta:
        model = State


class CityType(DjangoObjectType):
    class Meta:
        model = City


class Query(object):
    state = graphene.Field(StateType, id=graphene.Int(), name=graphene.String())
    all_states = graphene.List(StateType)
    city = graphene.Field(CityType, id=graphene.Int(), name=graphene.String())
    all_cities = graphene.List(CityType)

    def resolve_all_states(self, info, **kwargs):
        return State.objects.all()

    def resolve_all_cities(self, info, **kwargs):
        return City.objects.all()

    def resolve_state(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return State.objects.get(pk=id)
        if name is not None:
            return State.objects.get(name=name)

        return None

    def resolve_city(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return City.objects.get(pk=id)
        if name is not None:
            return City.objects.get(name=name)

        return None

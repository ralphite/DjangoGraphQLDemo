import graphene

import main.schema


class Query(main.schema.Query, graphene.ObjectType):
    pass


class Mutation(main.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

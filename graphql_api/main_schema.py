# cookbook/schema.py
import graphene
import users.schema 
import graphql_jwt


class Query(
    users.schema.Query, # Add Query objects here
    graphene.ObjectType
):
    pass

class Mutation(
    users.schema.Mutation, # Add Mutation objects here
    graphene.ObjectType):
    
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(query=Query, mutation=Mutation)

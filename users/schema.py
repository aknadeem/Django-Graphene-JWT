# cookbook/schema.py
import graphene
from graphene_django import DjangoObjectType

from graphql_jwt.decorators import login_required, staff_member_required

from django.contrib.auth import get_user_model
from users.models import User, Category, Ingredient


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        # fields = ("user_name", "email", "password","user_level")

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class Query(graphene.ObjectType):

    user = graphene.Field(UserType, id = graphene.Int(required=True))

    all_users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user

        if user.is_anonymous:
            raise Exception('Not Logged In!')

        return user

    @login_required
    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    @staff_member_required
    def resolve_all_users(self, info):
        # We can easily optimize query count in the resolve method
        return get_user_model().objects.all()


    # user = graphene.Field(UserType)

    # def resolve_user(self, args, context, info):
    #    if context.user.is_authenticated:
    #       return context.user

    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        user = get_user_model()(
            username=username,
            email=email,
            password=password,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()



# mutation {
#   tokenAuth(
#     username: "testuser",
#     password: "testuser"
#   ) {
#     token
#   }
# }
        
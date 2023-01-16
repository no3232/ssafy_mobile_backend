from graphene import relay, ObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view

class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        filter_fields = ['id', 'username', 'email']
        interfaces = (relay.Node, )

class Query(ObjectType):
    all_users = DjangoFilterConnectionField(UserNode)
    user = relay.Node.Field(UserNode)

    def resolve_all_users(self, info, **kwargs):
        return get_user_model().objects.all()


class Mutation(ObjectType):
    pass

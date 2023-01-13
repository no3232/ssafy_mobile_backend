import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from community.models import Community, Comment
import accounts.schema


class CommunityType(DjangoObjectType):
    class Meta:
        model = Community

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class Query(accounts.schema.Query, graphene.ObjectType):
    all_Communities = graphene.List(CommunityType)
    all_Comments = graphene.List(CommentType)

    def resolve_all_Communities(self, info, **kwargs):
        return Community.objects.all()
    
    def resolve_all_Comments(self, info, **kwargs):
        return Comment.objects.all()

class Mutation(
    accounts.schema.Mutation, # Add your Mutation objects here
    graphene.ObjectType
):
    pass

# schema = graphene.Schema(query=Query, mutation=Mutation)
schema = graphene.Schema(query=Query)
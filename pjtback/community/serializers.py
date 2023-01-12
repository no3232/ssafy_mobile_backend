from rest_framework import serializers
from .models import Community, Comment , ArticleImage, Travelpath, Like

class CommunityListSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Community
        fields = '__all__'

class CommunitySerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Community
        fields = '__all__'
        read_only_fields = ('user',)


class CommentSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user',)


class ArticleImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ArticleImage
        fields = '__all__'


class TravelPathSerializer(serializers.ModelSerializer):

    class Meta:
        model = Travelpath
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

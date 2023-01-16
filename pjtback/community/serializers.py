from rest_framework import serializers
from .models import Board, Travel ,Place 

class PlaceSerializer(serializers.ModelSerializer):
    placeId = serializers.IntegerField(source='id')

    class Meta:
        model = Place
        fields = ('placeId','placeName','saveDate','memo','placeImgList','latitude','longitude','address',)

class TravelSerializer(serializers.ModelSerializer):
    travelId = serializers.IntegerField(source='id')

    placeList = PlaceSerializer(many=True, read_only= True)

    class Meta:
        model = Travel
        fields = ('travelId','location','startDate','endDate','theme', 'placeList',)
        read_only_fields = ('placeList',)


class BoardListSerializer(serializers.ModelSerializer):
    boardId = serializers.IntegerField(source='id')

    userId = serializers.IntegerField(source ='userId.pk', read_only=True)
    nickname =  serializers.CharField(source='userId.nickname', read_only=True)
    travel = TravelSerializer(many=True,read_only= True)

    class Meta:
        model = Board
        fields = ('BoardId','userId','nickname', 'profileImg','writeDate','title','content','imageList','travel','likeCount','commentCount',)
        read_only_fields = ('userId','travel',)



# class CommunityListSerializer(serializers.ModelSerializer):

#     username = serializers.CharField(source='user.username', read_only=True)

#     class Meta:
#         model = Community
#         fields = '__all__'

# class CommunitySerializer(serializers.ModelSerializer):

#     username = serializers.CharField(source='user.username', read_only=True)

#     class Meta:
#         model = Community
#         fields = '__all__'
#         read_only_fields = ('user',)


# class CommunityCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Community
#         fields = ('title','content','secret_type','travel_region','travel_start_date','travel_end_date','travel_theme','is_creating','travel_length',)


# class CommentSerializer(serializers.ModelSerializer):

#     username = serializers.CharField(source='user.username', read_only=True)

#     class Meta:
#         model = Comment
#         fields = '__all__'
#         read_only_fields = ('user',)


# class ArticleImageSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = ArticleImage
#         fields = '__all__'


# class TravelPathSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Travelpath
#         fields = '__all__'

# class LikeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Like
#         fields = '__all__'

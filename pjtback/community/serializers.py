from rest_framework import serializers
from .models import Board, Travel ,Place , Comment, Like 

class PlaceSerializer(serializers.ModelSerializer):
    placeId = serializers.IntegerField(source='id')
    saveDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    placeImgList = serializers.JSONField(required=False)

    class Meta:
        model = Place
        fields = ('placeId','placeName','saveDate','memo','placeImgList','latitude','longitude','address',)


class TravelSerializer(serializers.ModelSerializer):
    # userId = serializers.IntegerField(source='userId.id', read_only=True)
    travelId = serializers.IntegerField(source='id', required=False, read_only=True)
    placeList = PlaceSerializer(many=True, required = False, allow_null = True ,read_only=True)
    startDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    endDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Travel
        fields = ( 'travelId','location','startDate','endDate','placeList',)
        read_only_fields = ('placeList',)
        


class BoardListSerializer(serializers.ModelSerializer):
    boardId = serializers.IntegerField(source='id', read_only=True)
    userId = serializers.IntegerField(source ='userId.pk', read_only=True)
    nickname =  serializers.CharField(source='userId.nickname', read_only=True)
    profileImg = serializers.ImageField(source = 'user.profileImg', read_only= True)
    writeDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only= True)
    travel = TravelSerializer()
    imageList = serializers.JSONField(required=False)

    class Meta:
        model = Board
        fields = ('boardId','userId','nickname', 'profileImg','writeDate','theme','title','content','imageList','travel','likeCount','commentCount',)
        read_only_fields = ('userId','travel','profileImg','writeDate',)

    

    # 요거는 혹시나 해서 참고로 남겨 둠
    # def create(self, validated_data):
    #     instance = Board.objects.create(**validated_data)
    #     image_set = self.context['request'].FILES
    #     for image_data in image_set.getlist('imageList'):
    #         Imagelist.objects.create(board=instance, image=image_data)
    #     return instance


class CommentSerializer(serializers.ModelSerializer):
    commentId = serializers.IntegerField(source='id', read_only=True)
    boardId = serializers.IntegerField(source='board.pk', read_only=True)
    userId = serializers.CharField(source='user.pk', read_only=True)
    nickname = serializers.CharField(source = 'user.nickname', read_only = True)
    profileImg = serializers.ImageField(source = 'user.profileImg')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user',)

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
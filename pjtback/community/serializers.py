from rest_framework import serializers
from .models import Board, Travel ,Place ,Imagelist, PlaceImage, Comment, Like , CharImage

class ImageSerializer(serializers.RelatedField):
    image = serializers.ImageField(use_url = True)

    def to_representation(self, instance):
        url = instance.image.url
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    class Meta:
        model = Imagelist
        fields = ('image',)

class CharImageSerializer(serializers.RelatedField):

    class Meta:
        model = CharImage
        fields = ('char_image',)


class PlaceImageSerializer(serializers.RelatedField):
    image = serializers.ImageField(use_url = True)

    def to_representation(self, instance):
        url = instance.image.url
        request = self.context.get('request', None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url

    class Meta:
        model = PlaceImage
        fields = ('image')

class PlaceSerializer(serializers.ModelSerializer):
    placeId = serializers.IntegerField(source='id')
    saveDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    placeImgList = PlaceImageSerializer(many=True , read_only = True)

    class Meta:
        model = Place
        fields = ('placeId','placeName','saveDate','memo','placeImgList','latitude','longitude','address',)

    def create(self, validated_data):
        instance = Place.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('imageList'):
            PlaceImage.objects.create(place=instance, image=image_data)
        return instance

class TravelSerializer(serializers.ModelSerializer):
    travelId = serializers.IntegerField(source='id')
    placeList = PlaceSerializer(many=True, required = False, allow_null = True)
    startDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    endDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Travel
        fields = ('travelId','location','startDate','endDate','placeList',)
        read_only_fields = ('placeList',)
        


class BoardListSerializer(serializers.ModelSerializer):
    boardId = serializers.IntegerField(source='id', read_only=True)
    userId = serializers.IntegerField(source ='userId.pk', read_only=True)
    nickname =  serializers.CharField(source='userId.nickname', read_only=True)
    travel = TravelSerializer(required=False, allow_null = True)
    writeDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only= True)
    imageList = serializers.JSONField(source='char_image_lst', required=False)
    profileImg = serializers.CharField(source = 'char_profile_img')

    class Meta:
        model = Board
        fields = ('boardId','userId','nickname', 'profileImg','writeDate','theme','title','content','imageList','travel','likeCount','commentCount',)
        read_only_fields = ('userId','travel','profileImg','writeDate',)
    
    def create(self, validated_data):
        instance = Board.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('imageList'):
            Imagelist.objects.create(board=instance, image=image_data)
        return instance


class CommentSerializer(serializers.ModelSerializer):
    commentId = serializers.IntegerField(source='id', read_only=True)
    boardId = serializers.IntegerField(source='board.pk', read_only=True)
    userId = serializers.CharField(source='user.pk', read_only=True)
    nickname = serializers.CharField(source = 'user.nickname', read_only = True)
    profileImg = serializers.CharField(source = 'user.profileImg')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user',)

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

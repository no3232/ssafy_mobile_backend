from rest_framework import serializers
from .models import Board, Travel ,Place ,Imagelist, PlaceImage

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
        for image_data in image_set.getlist('image'):
            PlaceImage.objects.create(place=instance, image=image_data)
        return instance

class TravelSerializer(serializers.ModelSerializer):
    travelId = serializers.IntegerField(source='id')
    placeList = PlaceSerializer(many=True, read_only= True)
    startDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    endDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Travel
        fields = ('travelId','location','startDate','endDate','theme', 'placeList',)
        read_only_fields = ('placeList',)
        


class BoardListSerializer(serializers.ModelSerializer):
    boardId = serializers.IntegerField(source='id', read_only=True)
    userId = serializers.IntegerField(source ='userId.pk', read_only=True)
    nickname =  serializers.CharField(source='userId.nickname', read_only=True)
    travel = TravelSerializer(read_only = True)
    writeDate = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only= True)
    imageList = ImageSerializer(many=True , read_only = True)

    class Meta:
        model = Board
        fields = ('boardId','userId','nickname', 'profileImg','writeDate','title','content','imageList','travel','likeCount','commentCount',)
        read_only_fields = ('userId','travel','profileImg','writeDate',)
    
    def create(self, validated_data):
        instance = Board.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            Imagelist.objects.create(board=instance, image=image_data)
        return instance



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

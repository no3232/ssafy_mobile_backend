from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
# from .serializers import  CommunityListSerializer, CommunitySerializer, CommentSerializer, ArticleImageSerializer , TravelPathSerializer, LikeSerializer, CommunityCreateSerializer
from .serializers import BoardListSerializer, ImageSerializer
from .models import Board  , Place ,Imagelist
from django.contrib.auth import get_user_model

# json 파싱을 위해서
import json

#for swagger
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiExample,inline_serializer
from rest_framework.decorators import api_view
from rest_framework import serializers



# for db orm query
from django.db.models import Q

@extend_schema(responses=BoardListSerializer(many=True), summary='게시글 전체 가져오기')
@api_view(['GET'])
def board_get(request):
    boards = Board.objects.all()
    serializer = BoardListSerializer(boards, many=True)
    return Response(serializer.data)

@extend_schema(request=BoardListSerializer(), summary='게시글 생성')
@api_view(['POST'])
def board_create(request):
    User = get_user_model()
    user = User.objects.get(pk=request.POST['user'])
    
    serializer = BoardListSerializer(data=request.data, context = {'request' : request})
    if serializer.is_valid(raise_exception=True):
        serializer.save(userId=user)
         
        return Response(serializer.data, status=status.HTTP_201_CREATED)





# @extend_schema(responses=CommunityListSerializer(many=True), summary='커뮤니티 게시글 개요 목록')
# @api_view(['GET'])
# def community_list(request):
#     # 요 user 는 postman test 용 user 나중에 request.user 로 바꿀 것.
    # User = get_user_model()
    # user = User.objects.get(pk=request.POST['user'])

#     community = Community.objects.all()
#     serializer = CommunityListSerializer(community, many=True)
#     return Response(serializer.data)


# @extend_schema(request =inline_serializer(name="a",fields={"filter": serializers.ListField(), "sort_option" : serializers.StringRelatedField()}), responses=CommunityListSerializer(many=True), summary='커뮤니티 게시글 개요 목록')
# @api_view(['POST'])
# def community_filtered_list(request):
#     # 요 user 는 postman test 용 user 나중에 request.user 로 바꿀 것.
#     User = get_user_model()
#     user = User.objects.get(pk=request.POST['user'])

#     # 대충 이런식으로 Q 들어가서 쿼리 조회 하면 된다.
#     # 알고리즘 적으로 좀만 생각해서 여기 추가 구현할 것.
#     community = get_list_or_404(Community, Q(title__contains=request.GET['filter']))

#     serializer = CommunityListSerializer(community, many=True)
#     return Response(serializer.data)


# @extend_schema(request=CommunityCreateSerializer,responses=inline_serializer(name="a",fields={"status": serializers.StringRelatedField()}),summary='게시글 생성')
# @api_view(['POST'])
# def community_create(request):
#     # 요 user 는 postman test 용 user 나중에 request.user 로 바꿀 것.
#     User = get_user_model()
#     user = User.objects.get(pk=request.POST['user'])

#     serializer = CommunitySerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(user=user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @extend_schema(request=CommunitySerializer,responses=CommunitySerializer,summary='게시글 상세, 삭제, 수정')
# @api_view(['GET', 'PUT', 'DELETE'])
# def community_detail(request, community_pk):
#     community = get_object_or_404(Community, pk=community_pk)
    
#     if request.method == 'GET':
#         serializer = CommunitySerializer(community)
#         return Response(serializer.data)

#     elif request.method == 'DELETE':
#         community.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     elif request.method == 'PUT':
#         serializer = CommunitySerializer(community, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user)
#             return Response(serializer.data)


# @extend_schema(responses=CommentSerializer(many=True),summary='코멘트 리스트 목록')
# @api_view(['GET'])
# def comment_list(request,community_pk):
#     if request.method == 'GET':
#         comments = Comment.objects.filter(community_id = community_pk)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)

# @extend_schema(responses = CommentSerializer , request=None ,summary='코멘트 생성')
# @api_view(['POST'])
# def comment_create(request, community_pk):
#     community = Community.objects.get(pk=community_pk)
#     serializer = CommentSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save(community=community, user=request.user)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @extend_schema(responses = CommentSerializer ,request=None,summary='코멘트 수정, 삭제')
# @api_view(['DELETE', 'PUT'])
# def comment_detail(request, comment_pk):
#     comment = get_object_or_404(Comment, pk=comment_pk)

#     if request.method == 'DELETE':
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
#     elif request.method == 'PUT':
#         community = Community.objects.get(pk=request.data['community_pk'])
#         serializer = CommentSerializer(comment, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user, community=community)
#             return Response(serializer.data)


# @extend_schema(request=ArticleImageSerializer , responses = ArticleImageSerializer ,summary='게시글 이미지 얻기, 생성')
# @api_view(['GET', 'POST'])
# def community_image(request, community_pk):
#     article_image = get_list_or_404(ArticleImage, pk = community_pk)
#     community = Community.objects.get(pk = community_pk)
#     if request.method == 'GET':
#         serializer = ArticleImageSerializer(article_image)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ArticleImageSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(community=community, user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# @extend_schema(responses = TravelPathSerializer ,summary='여행 경로 저장된 포인트들 얻기')
# @api_view(['GET'])
# def travelpath(request, community_pk):
#     travel_path = get_object_or_404(Travelpath, pk=community_pk)
#     if request.method == 'GET':
#         serializer = TravelPathSerializer(travel_path)
#         return Response(serializer.data)

# @extend_schema(responses=None, summary='여행 시작 버튼 누르기 내부적으로는 빈 커뮤니티와 여행경로 gps 정보 저장을 위한 리스트 생성')
# @api_view(['POST'])
# def traval_start(request):
#     #여행 시작 누를 때 먼저 community 부터 생성한다음 배정해줌
#     community = Community.objects.create()
#     serializer = TravelPathSerializer()

#     if serializer.is_valid(raise_exception=True):
#         serializer.save(communitiy=community , user = request.user)
#         return Response(status=status.HTTP_201_CREATED)

# @extend_schema(request =inline_serializer(name="a",fields={"latitude": serializers.FloatField() , "longitude": serializers.FloatField()}),summary='gps 정보를 담아서 보내 주실 경로')
# @api_view(['POST'])
# def travel_point_collect(request, community_pk):
#     travel_path_recording = get_object_or_404(Travelpath, pk=community_pk)
#     travel_point_lst = travel_path_recording.travel_point_lst
#     point_dic = {}
#     #파싱
#     point_dic = json.loads(travel_point_lst)
#     point_lst = []

#     for key, value in point_dic.items():
#         point_lst.append(value)

#     point_lst.append(request.POST['point'])
#     # 다시 json
#     point_dic = {}
#     for i in range(len(point_lst)):
#         point_dic[i] = point_lst[i]
    
#     travel_point_lst = json.dumps(point_dic)
#     travel_path_recording.travel_point_lst = travel_point_lst

#     serializer = TravelPathSerializer(travel_path_recording)

#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#         return Response(status=status.HTTP_200_OK)


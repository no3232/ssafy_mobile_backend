from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import requests

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import  CommunityListSerializer, CommunitySerializer, CommentSerializer, ArticleImageSerializer , TravelPathSerializer, LikeSerializer
from .models import Community, Comment, ArticleImage, Travelpath, Like
from django.contrib.auth import get_user_model

# json 파싱을 위해서
import json

#for swagger
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiExample,inline_serializer
from rest_framework.decorators import api_view
from rest_framework import serializers


@extend_schema(request=inline_serializer(name="a",fields={"community_pk": serializers.CharField()}), responses=CommunityListSerializer, summary='커뮤니티 게시글 개요 목록')
@api_view(['GET', 'POST'])
def community_list(request):
    User = get_user_model()
    user = User.objects.get(pk=request.POST['user'])

    if request.method == 'GET':
        community = Community.objects.all()
        serializer = CommunityListSerializer(community, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE', 'PUT'])
def community_detail(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    
    if request.method == 'GET':
        serializer = CommunitySerializer(community)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        serializer = CommunitySerializer(community, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)

@api_view(['GET', 'POST'])
def comment_list(request,community_pk):
    if request.method == 'GET':
        comments = Comment.objects.filter(community_id = community_pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        community = Community.objects.get(pk=community_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(community=community, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'DELETE', 'PUT'])
def comment_detail(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        community = Community.objects.get(pk=request.data['community_pk'])
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, community=community)
            return Response(serializer.data)


@api_view(['GET', 'POST'])
def community_image(request, community_pk):
    article_image = get_list_or_404(ArticleImage, pk = community_pk)
    community = Community.objects.get(pk = community_pk)
    if request.method == 'GET':
        serializer = ArticleImageSerializer(article_image)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ArticleImageSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(community=community, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def travelpath(request, community_pk):
    travel_path = get_object_or_404(Travelpath, pk=community_pk)
    if request.method == 'GET':
        serializer = TravelPathSerializer(travel_path)
        return Response(serializer.data)

# 일단 완성 path 가 어떤 꼴일지는 모르겠는데 get 요청만 두고 주고, 이 밑에 travelpath point 받아오는 api 같은거 만들어야 할듯?

@api_view(['POST'])
def traval_start(request):
    #여행 시작 누를 때 먼저 community 부터 생성한다음 배정해줌
    community = Community.objects.create()
    serializer = TravelPathSerializer()

    if serializer.is_valid(raise_exception=True):
        serializer.save(communitiy=community , user = request.user)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def travel_point_collect(request, community_pk):
    travel_path_recording = get_object_or_404(Travelpath, pk=community_pk)
    travel_point_lst = travel_path_recording.travel_point_lst
    point_dic = {}
    #파싱
    point_dic = json.loads(travel_point_lst)
    point_lst = []

    for key, value in point_dic.items():
        point_lst.append(value)

    point_lst.append(request.POST['point'])
    # 다시 json
    point_dic = {}
    for i in range(len(point_lst)):
        point_dic[i] = point_lst[i]
    
    travel_point_lst = json.dumps(point_dic)
    travel_path_recording.travel_point_lst = travel_point_lst

    serializer = TravelPathSerializer(travel_path_recording)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_200_OK)


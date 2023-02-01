from django.db.models import F
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import BoardListSerializer, PlaceSerializer, TravelSerializer , CommentSerializer
from .models import Board, Place, Travel, Comment
from django.contrib.auth import get_user_model

# json 파싱을 위해서
import json

# for swagger
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiExample, inline_serializer
from rest_framework.decorators import api_view
from rest_framework import serializers

# for db orm query
from django.db.models import Q



from firebase_admin import messaging

# fire base message를 위한 함수
def send_to_firebase_cloud_messaging():
    # This registration token comes from the client FCM SDKs.
    registration_token = 'dLlc4_JMRMuYtetSRj_TGV:APA91bGFHN2uGRV6Mn8OCRmMRQ-sOECODMGjDS7F14sqxOIBxhnb7e2b52dykkrZ3MQTPbZYw-F63OyExJVToeUasfwlv-p8-xT3TVvXXVhA8WrzKWSoC9AjJRa2kjFFeSC-8lWeCHZM'   # 이걸 해야 되는데.

    # See documentation on defining a message payload.
    message = messaging.Message(
    notification=messaging.Notification(
        title='안녕하세요 타이틀 입니다',
        body='안녕하세요 메세지 입니다',
    ),
    token=registration_token,
    )

    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)


@extend_schema(responses=BoardListSerializer(many=True), summary='게시글 전체 가져오기')
@api_view(['GET'])
def board_get(request):
    boards = Board.objects.all()
    serializer = BoardListSerializer(boards, many=True, context={"request": request})
    return Response(serializer.data)



@extend_schema(request=BoardListSerializer(), summary='게시글 생성')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def board_create(request):
    user = request.user
    
    serializer = BoardListSerializer(data=request.data)
    wanted_travel = get_object_or_404(Travel, pk=request.data['travel']['travelId'])
    
    if serializer.is_valid(raise_exception=True):
        serializer.save(userId=user, travel=wanted_travel)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 쿼리 형식으로 db 접근 할 수 있는 라이브러리
from django.db.models import Q, F
from datetime import timedelta

@extend_schema(summary='게시글 필터 필터 부분 바디에 담아서 보내주시면 됨')
@api_view(['POST'])
def board_filtered(request):
    boards = Board.objects.annotate(
        day=F('travel__endDate') - F('travel__startDate'))
    # 기본 전략은 4가지 필터 부분으로 분리하고, get 으로 접근
    # get 했을 때 none 이면 필터 pass 하는 식
    age = request.data.get('ageList')
    periods = request.data.get('periodList')
    theme = request.data.get('themeList')
    region = request.data.get('regionList')

    boards = Board.objects.annotate(day = F('travel__endDate') - F('travel__startDate'))

    # 일단 하드 코딩에 가깝긴 한데, 프엔에서 넘겨주는 타이밍 까지 만드는게 아니면 그냥 이런식으로 쓰고 수정하는게 나을듯?
    age_dic = { '10대' : [10,20], '20대': [20,30] , '30대' : [30,40] , '40대': [40,50], '50대': [50,60], '60대 이상': [60,100]}
    periods_dic = {'당일 치기': 1, '1박 2일': 2, '3박 4일': 3, '4박 5일+': 4}
    theme_lst = ['혼자', '친구와', '연인과', '배우자와', '아이와', '부모님과', '기타']
    region_lst = ["서울","경기","강원","부산","경북·대구","전남·광주","제주","충남·대전","경남","충북","경남","전북","인천"]


    # alyways true q object 찾아보니까 이렇더라 이거 default로 추가해가면 될 것 같음.
    # result_query = ~Q(pk__in=[])
    age_query = Q(pk__in=[])
    period_query = Q(pk__in=[])
    theme_query = Q(pk__in=[])
    region_query = Q(pk__in=[])

    if age:
        for age_str in age:
            age_query  |= Q(userId__age__gte = age_dic[age_str][0] , userId__age__lt = age_dic[age_str][1])
    else:
        age_query = ~Q(pk__in=[])
    
    if periods:
        for period_str in periods:
            period_query |= Q(day__lt = timedelta(days=periods_dic[period_str]))
    else:
        period_query = ~Q(pk__in=[])

    if theme:
        for theme_str in theme:
            theme_query |= Q(theme = theme_str)
    else:
        theme_query = ~Q(pk__in=[])

    if region:    
        for region_str in region:
            region_query |= Q(travel__location__contains = region_str)
    else:
        region_query = ~Q(pk__in=[])
    
    result_query = age_query & period_query & theme_query & region_query
    result_board = boards.filter(result_query)

    serializer = BoardListSerializer(result_board, many= True, context={"request": request})

    return Response(serializer.data, status= status.HTTP_200_OK)

@extend_schema(responses=TravelSerializer(many = True), summary='게시글 전체 조회')
@api_view(['GET'])
def travel_get(request):
    travels = Travel.objects.all()
    serializer = TravelSerializer(travels, many=True)
    return Response(serializer.data)


@extend_schema(request=TravelSerializer(), summary='단일 게시글 조회 수정 삭제')
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def travel_detail(request, travel_id):
    travel = get_object_or_404(Travel, id = travel_id)
    if request.method == 'GET':
        serializer = TravelSerializer(travel)
        return Response(serializer.data)

    elif request.method == 'PUT':
        user = request.user
        if travel.userId == user:
            serializer = TravelSerializer(travel, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(userId = user)
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)  
    
    elif request.method == 'DELETE':
        if request.user == travel.userId:
            travel.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(request=TravelSerializer(), summary='여정 생성')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def travel_create(request):
    user = request.user
    serializer = TravelSerializer(data=request.data, context ={'request': request})
    if serializer.is_valid(raise_exception=True):
        serializer.save(userId=user)

        return Response(status=status.HTTP_201_CREATED)


@extend_schema(summary='user_id 파라미터로 넣어 주면 해당 유저의 travel')
@api_view(['GET'])
def travel_user(request, user_id):
    travels = Travel.objects.filter(userId__id = user_id)
    serializer = TravelSerializer(travels, many = True)

    return Response(serializer.data)

@extend_schema(summary='Board 상세페이지 조회, 수정, 삭제')
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def board_detail(request, board_id):

    board = get_object_or_404(Board, id = board_id)
    if request.method == 'GET':
        serializer = BoardListSerializer(board, context={"request": request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        user = request.user
        if board.userId == user:
            wanted_travel = get_object_or_404(Travel, pk=request.data['travel']['travelId'])
            serializer = BoardListSerializer(board, data=request.data, context={"request": request})
            if serializer.is_valid(raise_exception=True):
                serializer.save(userId=user, travel=wanted_travel)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)  
    
    elif request.method == 'DELETE':
        if request.user == board.userId:
            board.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, board_id):
    board = Board.objects.get(id = board_id)
    user = request.user

    if board.likeList.filter(id=request.user.id).exists():
        board.likeList.remove(user)
        return Response(data = False,status=status.HTTP_202_ACCEPTED)
    else:
        board.likeList.add(user)
        return Response(data = True, status=status.HTTP_202_ACCEPTED)

@extend_schema(responses = CommentSerializer , request=CommentSerializer ,summary='코멘트 생성')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, board_id):
    board = Board.objects.get(id=board_id)
    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(board=board, user=request.user)
        board_modified = Board.objects.get(id = board_id)
        boardserializer = BoardListSerializer(board_modified, context={"request": request})
        
        return Response(boardserializer.data, status=status.HTTP_201_CREATED)

@extend_schema(responses = CommentSerializer , request=CommentSerializer ,summary='코멘트 수정, 삭제')
@api_view(['DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def comments(request,board_id,comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'DELETE':
        comment.delete()
        board_modified = Board.objects.get(id = board_id)
        boardserializer = BoardListSerializer(board_modified, context={"request": request})
        return Response(boardserializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        comment = Comment.objects.get(id=comment_id)
        board = Board.objects.get(id = board_id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, board=board)
            board_modified = Board.objects.get(id = board_id)
            boardserializer = BoardListSerializer(board_modified, context={"request": request})
            return Response(boardserializer.data, status=status.HTTP_202_ACCEPTED)





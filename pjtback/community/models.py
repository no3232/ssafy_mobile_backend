from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Board(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='writeBoard')
    writeDate = models.DateTimeField(auto_now = True)
    theme = models.CharField(max_length=20, default='')
    title = models.CharField(max_length= 50 , default="")
    content = models.TextField(max_length=300)
    likeCount = models.IntegerField(_("likeCount"), default=0)
    commentCount = models.IntegerField(_("commentCount"), default=0)
    like_user = models.ManyToManyField(User, related_name='myLikeBoard')
    char_profile_img = models.CharField(max_length=100)
    char_image_lst = models.JSONField()

    
class Travel(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='travel')
    board = models.OneToOneField(Board, on_delete=models.CASCADE,related_name='travel')
    location = models.CharField(max_length=30, default='')
    startDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDate = models.DateTimeField(auto_now=False, auto_now_add=False)

class Place(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='placeList')
    placeName = models.CharField(max_length = 20, default="대구")
    saveDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    memo = models.CharField(max_length=20)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    address = models.CharField(max_length=40, default='')


def image_upload_path():
    return f'profile_image/boards/%Y/%m'

class Imagelist(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE , related_name = 'imageList')
    image = ProcessedImageField(
        blank=True,
        upload_to=image_upload_path(),
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 70},
)

class CharImage(models.Model):
    char_image = models.CharField(max_length=100)


class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE , related_name= 'placeImgList')
    image = ProcessedImageField(
        blank=True,
        upload_to='profile_image/place/%Y/%m',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 70},
    )

class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length = 30)
    content = models.TextField(max_length=34)
    write_date = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)


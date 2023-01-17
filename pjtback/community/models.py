from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.




class Board(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='writeBoard')
    profileImg = ProcessedImageField(
        blank=True,
        upload_to='profile_image/board/profile/%Y/%m',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 70},
    )
    writeDate = models.DateTimeField(auto_now = True)
    title = models.CharField(max_length= 50 , default="")
    content = models.TextField(max_length=300)
    likeCount = models.IntegerField(_("likeCount"), default=0)
    commentCount = models.IntegerField(_("commentCount"), default=0)
    like_user = models.ManyToManyField(User, related_name='myLikeBoard')

    
class Travel(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='travel')
    board = models.OneToOneField(Board, on_delete=models.CASCADE,related_name='travel')
    location = models.CharField(max_length=30, default='')
    startDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDate = models.DateTimeField(auto_now=False, auto_now_add=False)
    theme = models.CharField(max_length=20, default='')

class Place(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='placeList')
    placeName = models.CharField(max_length = 20, default="대구")
    saveDate = models.DateTimeField(auto_now=False)
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


class PlaceImage(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE , related_name= 'placeImgList')
    image = ProcessedImageField(
        blank=True,
        upload_to='profile_image/place/%Y/%m',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 70},
    )

# class ArticleImage(models.Model):
#     img_url = models.ImageField(_("article_image_url"))
#     Community = models.ForeignKey(Community, on_delete=models.CASCADE)

# class Comment(models.Model):
#     community = models.ForeignKey(Community, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     content = models.TextField(max_length=34)
#     created_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)

# class Travelpath(models.Model):
#     community = models.ForeignKey(Community, on_delete=models.CASCADE)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     travel_point_lst = models.JSONField(_("travel_point_json"),default=dict)
#     # 혹시나 지도 위에다 그리는 거면 필요 없는 필드가 될 수도 있음.
#     travel_created_img_url = models.ImageField(_("travel_created_img_url"))


# class Like(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     community = models.ForeignKey(Community, on_delete=models.CASCADE)


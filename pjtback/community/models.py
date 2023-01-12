from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Community(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    content = models.TextField(max_length=200)
    secret_type = models.BooleanField(_("secret_type"), default=False)
    secret_password = models.CharField(_("article_password"), max_length=20, default="")
    travel_region = models.CharField(_("region"), max_length=50)
    travel_start_date = models.DateTimeField(_("start_date"), auto_now=False, auto_now_add=False)    
    travel_end_date = models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)
    is_creating = models.BooleanField(_("is_creating"), default = False)
    travel_length = models.FloatField(_("travel_lenth"))
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class ArticleImage(models.Model):
    img_url = models.ImageField(_("article_image_url"))
    Community = models.ForeignKey(Community, on_delete=models.CASCADE)

class Comment(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(max_length=34)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Travelpath(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    travel_point_lst = models.JSONField(_("travel_point_json"),default=dict)
    # 혹시나 지도 위에다 그리는 거면 필요 없는 필드가 될 수도 있음.
    travel_created_img_url = models.ImageField(_("travel_created_img_url"))


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)


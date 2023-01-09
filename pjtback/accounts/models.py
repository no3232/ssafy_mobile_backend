from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(_("email_address"), unique=True)
    phone_number = models.CharField(_("phone"), max_length=13)
    profile_image = ProcessedImageField(
        blank=True,
        upload_to='profile_image/%Y/%m',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 70},
    )
    naver_email = models.EmailField(_("naver_email"), null=True)
    kakao_email = models.EmailField(_("kakao_email"), null=True)
    google_email = models.EmailField(_("google_email"), null=True)

    

from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
class User(AbstractUser):
    # profile_image = ProcessedImageField(
    #     blank=True,
    #     upload_to='profile_image/%Y/%m',
    #     processors=[ResizeToFill(300, 300)],
    #     format='JPEG',
    #     options={'quality': 70},
    # )
    pass
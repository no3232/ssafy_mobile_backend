# Generated by Django 3.2.13 on 2023-01-16 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_age'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='google_email',
            new_name='google',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='kakao_email',
            new_name='kakao',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='naver_email',
            new_name='naver',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='profile_image',
            new_name='profileImg',
        ),
    ]

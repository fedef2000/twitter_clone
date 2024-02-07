# Generated by Django 5.0.1 on 2024-02-07 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_tweet_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfollowing',
            old_name='following_user_id',
            new_name='following',
        ),
        migrations.RenameField(
            model_name='userfollowing',
            old_name='user_id',
            new_name='profile',
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='defaultProfileImage.jpg', upload_to='profile_photo'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='tweet_photo'),
        ),
    ]

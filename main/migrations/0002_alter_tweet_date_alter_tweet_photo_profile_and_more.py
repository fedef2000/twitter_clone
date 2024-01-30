# Generated by Django 5.0.1 on 2024-01-30 16:08

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pic'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('photo', models.ImageField(blank=True, default='defaultProfileImage.jpg', upload_to='profile_pic')),
                ('bio', models.TextField(blank=True, max_length=500, null=True)),
                ('follow', models.ManyToManyField(blank=True, to='main.profile')),
            ],
        ),
        migrations.AlterField(
            model_name='tweet',
            name='likedBy',
            field=models.ManyToManyField(blank=True, related_name='likedTweet', to='main.profile'),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='main.profile'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
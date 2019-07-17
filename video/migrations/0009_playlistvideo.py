# Generated by Django 2.2.1 on 2019-07-08 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0008_genrevideo_popgenrevideo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_code', models.CharField(max_length=20)),
                ('playlist_code', models.CharField(max_length=20)),
                ('playlist_name', models.CharField(max_length=200)),
                ('type', models.PositiveIntegerField(default=0)),
                ('chart', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=200)),
                ('artist', models.CharField(default='', max_length=200)),
                ('video_key', models.CharField(max_length=20)),
            ],
        ),
    ]

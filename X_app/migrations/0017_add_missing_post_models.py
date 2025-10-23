# Manually created migration to add missing post-related models

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('X_app', '0016_add_post_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text="Hashtag name without # (e.g., 'travel')", max_length=100, unique=True)),
                ('posts_count', models.PositiveIntegerField(default=0)),
                ('last_used', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-posts_count', 'name'],
            },
        ),
        migrations.CreateModel(
            name='PostView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('duration_seconds', models.PositiveIntegerField(default=0, help_text='How long the user viewed the post')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='X_app.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_views', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-viewed_at'],
                'unique_together': {('user', 'post')},
            },
        ),
        migrations.CreateModel(
            name='PostMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_file', models.FileField(upload_to='posts/media/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mov', 'avi', 'webm'])])),
                ('media_type', models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default='image', max_length=10)),
                ('order', models.PositiveIntegerField(default=0, help_text='Order of media in carousel')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_media', to='X_app.post')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('post', 'order')},
            },
        ),
    ]

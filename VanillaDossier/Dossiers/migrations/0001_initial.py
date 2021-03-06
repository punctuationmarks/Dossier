# Generated by Django 2.2.6 on 2019-11-13 14:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DossiersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hobbies', models.CharField(blank=True, max_length=300)),
                ('work', models.CharField(blank=True, max_length=300)),
                ('appearance', models.CharField(blank=True, max_length=100)),
                ('notable_memories', models.CharField(blank=True, max_length=100)),
                ('discussions', models.TextField(blank=True)),
                ('date_originally_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

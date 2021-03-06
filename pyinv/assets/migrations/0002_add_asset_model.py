# Generated by Django 3.2.13 on 2022-05-14 18:30

import uuid

import autoslug.fields  # type: ignore
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_add_manufacturer'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('slug', autoslug.fields.AutoSlugField(
                    default=None, editable=True, null=True, populate_from='name', unique=True,
                )),
                ('is_container', models.BooleanField(default=False, verbose_name='Can contain assets')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('manufacturer', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='assets.manufacturer',
                )),
            ],
        ),
    ]

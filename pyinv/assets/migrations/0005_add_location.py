# Generated by Django 3.2.13 on 2022-05-15 17:21

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_add_asset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asset', models.OneToOneField(
                    blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                    related_name='linked_location', to='assets.asset',
                )),
                ('parent', models.ForeignKey(
                    blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                    related_name='children_set', to='assets.location',
                )),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='asset',
            name='location',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, related_name='contents', to='assets.location',
            ),
        ),
    ]
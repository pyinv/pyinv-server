# Generated by Django 3.2.13 on 2022-07-07 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_remove_asset_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetcode',
            name='code_type',
            field=models.CharField(
                choices=[
                    ('A', 'Arbitrary String'),
                    ('D', 'Damm 32'),
                    ('S', 'Student Robotics'),
                ],
                max_length=1,
            ),
        ),
    ]

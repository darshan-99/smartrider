# Generated by Django 3.0.2 on 2020-03-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0023_auto_20200313_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabdriver',
            name='cdNumberplate',
            field=models.CharField(default='', max_length=20),
        ),
    ]

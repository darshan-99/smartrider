# Generated by Django 3.0.2 on 2020-03-13 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0024_cabdriver_cdnumberplate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cabdriver',
            name='cdNumberplate',
        ),
        migrations.AddField(
            model_name='cabdriver',
            name='cabdNumberplate',
            field=models.CharField(default='', max_length=20),
        ),
    ]

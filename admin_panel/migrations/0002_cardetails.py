# Generated by Django 3.0.2 on 2020-02-01 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cardetails',
            fields=[
                ('carID', models.AutoField(primary_key=True, serialize=False)),
                ('carName', models.CharField(max_length=30)),
                ('carCompany', models.CharField(max_length=20)),
                ('carType', models.CharField(max_length=30)),
                ('carCapicity', models.IntegerField()),
                ('carPic', models.CharField(max_length=20)),
                ('carFPH', models.IntegerField()),
                ('carFPKm', models.IntegerField()),
            ],
        ),
    ]

# Generated by Django 4.1.7 on 2023-04-06 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_date', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to='')),
                ('command', models.CharField(max_length=100)),
                ('sdate', models.DateTimeField()),
                ('status', models.CharField(max_length=20)),
            ],
        ),
    ]

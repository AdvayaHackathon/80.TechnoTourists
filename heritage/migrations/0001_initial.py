# Generated by Django 5.2 on 2025-04-11 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('region', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('etiquette', models.TextField()),
                ('festival_date', models.CharField(blank=True, max_length=200)),
                ('qr_info_link', models.URLField(blank=True)),
            ],
        ),
    ]

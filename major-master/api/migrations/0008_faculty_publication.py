# Generated by Django 3.2.16 on 2024-05-25 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20240524_0723'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('department', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('journal', models.CharField(max_length=255)),
                ('publication_date', models.DateField()),
                ('publication_year', models.PositiveIntegerField()),
                ('abstract', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('authors', models.ManyToManyField(related_name='publications', to='api.Faculty')),
            ],
        ),
    ]
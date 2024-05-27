# Generated by Django 3.2.16 on 2024-05-25 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20240525_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_type',
            field=models.CharField(choices=[('JOURNAL', 'Journal'), ('CONFERENCE', 'Conference'), ('BOOK', 'Book'), ('CHAPTER', 'Book Chapter'), ('OTHER', 'Other')], max_length=50),
        ),
    ]

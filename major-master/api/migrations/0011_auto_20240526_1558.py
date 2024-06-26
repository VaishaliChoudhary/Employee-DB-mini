# Generated by Django 3.2.16 on 2024-05-26 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20240525_1544'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name_plural': 'Faculties'},
        ),
        migrations.AddField(
            model_name='faculty',
            name='short_form',
            field=models.CharField(blank='True', max_length=50),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='expertise',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='qualification',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_type',
            field=models.CharField(choices=[('JOURNAL', 'Journal'), ('CONFERENCE', 'Conference'), ('ARTICLE', 'Article'), ('BOOK', 'Book'), ('OTHER', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_year',
            field=models.PositiveIntegerField(choices=[('1996', '1996'), ('1997', '1997'), ('1998', '1998'), ('1999', '1999'), ('2000', '2000'), ('2001', '2001'), ('2002', '2002'), ('2003', '2003'), ('2004', '2004'), ('2005', '2005'), ('2006', '2006'), ('2007', '2007'), ('2008', '2008'), ('2009', '2009'), ('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')]),
        ),
        migrations.AlterUniqueTogether(
            name='faculty',
            unique_together={('name', 'short_form')},
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='designation',
        ),
    ]

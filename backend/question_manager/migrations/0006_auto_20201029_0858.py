# Generated by Django 3.1.2 on 2020-10-29 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_manager', '0005_merge_20201028_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='target',
            field=models.CharField(choices=[('category', 'category'), ('questions', 'questions')], max_length=20),
        ),
    ]

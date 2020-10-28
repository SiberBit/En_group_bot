# Generated by Django 3.1.2 on 2020-10-27 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question_manager', '0003_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('slug', models.SlugField()),
                ('visibility', models.BooleanField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question_manager.organizations')),
            ],
        ),
        migrations.CreateModel(
            name='ChatBot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('platform', models.CharField(max_length=20)),
                ('link', models.URLField()),
                ('description', models.TextField(max_length=100)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='question_manager.departments')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='question_manager.organizations')),
            ],
        ),
    ]
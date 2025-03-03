# Generated by Django 5.0.12 on 2025-03-03 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='hired_employees',
            fields=[
                ('id_employ', models.IntegerField(primary_key=True, serialize=False)),
                ('name_employ', models.CharField(max_length=200)),
                ('datetime', models.CharField(max_length=200)),
                ('department_id', models.IntegerField()),
                ('job_id', models.IntegerField()),
            ],
        ),
    ]

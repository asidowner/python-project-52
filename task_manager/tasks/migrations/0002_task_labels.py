# Generated by Django 4.1.4 on 2022-12-21 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(related_name='labels', to='labels.tasklabel'),
        ),
    ]

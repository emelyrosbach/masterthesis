# Generated by Django 5.0.1 on 2024-02-04 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vue', '0011_alter_data_experiment_alter_poststudydata_experiment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingdata',
            name='confidence_scores',
        ),
    ]

# Generated by Django 5.0.1 on 2024-01-13 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vue', '0002_alter_experiment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='participant_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

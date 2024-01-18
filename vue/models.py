from django.db import models

class Order(models.Model):
    slide_order = models.CharField(max_length=20, unique=True)

class Experiment(models.Model):
    participant_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200, null=True)
    group= models.CharField(max_length=1)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, default='open')

    class Meta:
        verbose_name_plural = 'Experiments'

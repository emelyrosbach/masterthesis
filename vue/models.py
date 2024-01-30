from django.db import models
import random 

class Order(models.Model):
    #change max-length accoridng to new slide number
    slide_order = models.CharField(max_length=100, unique=True)

class Experiment(models.Model):
    participant_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=200, null=True)
    group= models.CharField(max_length=1)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200, default='open')

    class Meta:
        verbose_name_plural = 'Experiments'

class Data(models.Model):
    condition = models.CharField(max_length=100)
    slide_number = models.CharField(max_length=200)
    tcp_est = models.CharField(max_length=200)
    confidence_score = models.CharField(max_length=200)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

class PreStudy(models.Model):
    gender = models.CharField(max_length=10)
    age = models.CharField(max_length=10)
    experience = models.CharField(max_length=100)
    interest_in_tech = models.CharField(max_length=100)
    adoption_of_new_tech = models.CharField(max_length=100)
    familiarity_with_AI = models.CharField(max_length=100)
    experiment = models.OneToOneField(Experiment, on_delete=models.CASCADE)

class PostStudy(models.Model):
    condition = models.CharField(max_length=100)
    UEQ_answers = models.CharField(max_length=100)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

class Training(models.Model):
    condition = models.CharField(max_length=100)
    tcp_est = models.CharField(max_length=200)
    confidence_score = models.CharField(max_length=200)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

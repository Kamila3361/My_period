from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class PersonalInfo(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(
        validators=[
            MinValueValidator(10, message="Age must be at least 10 years old."),
            MaxValueValidator(85, message="Age must be at most 85 years old."),
        ]
    )
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.FloatField()
    cramps = models.IntegerField(
        validators=[
            MinValueValidator(0, message="I don't have pain."),
            MaxValueValidator(10, message="I have pain."),
        ]
    ) 
    feeling_tired = models.IntegerField(
        validators=[
            MinValueValidator(0, message="I don't have pain."),
            MaxValueValidator(10, message="I have pain."),
        ]
    ) 

class PeriodCycle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    cycle_length = models.IntegerField(default=5)

class ChatInfo(models.Model):
    ROLE_CHOICES = (
        ('assistant', 'assistant'),
        ('user', 'usser'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    content = models.TextField()


from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Expens(models.Model):
    name=models.CharField(max_length=150)
    date=models.DateField()
    category=models.CharField(choices=[('Health','Health'),(' Electronics',' Electronics'), ('Travel','Travel'), ('Education','Education'), ('Books','Books'),('Others','Others')],max_length=20)
    description=models.TextField()
    amount=models.PositiveIntegerField()
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


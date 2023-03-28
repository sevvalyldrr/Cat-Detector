from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Images(models.Model):
    name = models.CharField(max_length=64)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    images = models.ImageField(upload_to='images')
    

    def __str__(self):
        return self.name

    def save(self):
        super(Images, self).save()


class Nums(models.Model):
    id = models.AutoField(primary_key=True)
    cat_numbers = models.IntegerField(null=True)
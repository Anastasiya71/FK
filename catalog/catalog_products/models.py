from django.db import models
from django.db.models.deletion import CASCADE


class Category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('Category', blank=True,
                               null=True, on_delete=CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=CASCADE)

    def __str__(self):
        return self.name

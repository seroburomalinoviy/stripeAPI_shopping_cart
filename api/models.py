from django.db import models
# Create your models here.


class Order(models.Model):
    """Model represent the instance of the item"""
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.item.name


class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.name









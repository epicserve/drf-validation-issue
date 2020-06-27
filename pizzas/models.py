from django.db import models


class Crust(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    crust = models.ForeignKey('pizzas.Crust', on_delete=models.PROTECT)
    toppings = models.ManyToManyField('pizzas.Topping', related_name='toppings')


class ToppingType(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Topping(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey('pizzas.ToppingType', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} ({self.type})'

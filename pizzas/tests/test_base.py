from django.test import TestCase

from pizzas.models import Crust, Topping, ToppingType


class BasePizzaTest(TestCase):

    def create_toppings(self):
        self.crust = Crust.objects.create(name='Original', slug='original')
        self.meat = ToppingType.objects.create(name='Meat', slug='meat')
        self.cheese = ToppingType.objects.create(name='Cheese', slug='cheese')
        self.sauce = ToppingType.objects.create(name='Sauce', slug='sauce')
        self.pepperoni = Topping.objects.create(name='Pepperoni', type=self.meat)
        self.mozzarella = Topping.objects.create(name='Mozzarella', type=self.cheese)
        self.marinara = Topping.objects.create(name='Marinara', type=self.sauce)

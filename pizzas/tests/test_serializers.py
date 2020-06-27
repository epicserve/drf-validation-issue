from django.test import TestCase
from django.urls import reverse

from pizzas.serializers import PizzaSerializer
from pizzas.tests.test_base import BasePizzaTest


class TestPizzaSerializer(BasePizzaTest):

    def setUp(self):
        self.create_toppings()

    def test_valid_data(self):
        pizza_serializer = PizzaSerializer(data={
            'name': 'Pepperoni',
            'price': '12.99',
            'crust': reverse('crust-detail', args=(self.crust.pk, )),
            'toppings': [
                reverse('topping-detail', args=(self.pepperoni.pk, )),
                reverse('topping-detail', args=(self.mozzarella.pk, )),
                reverse('topping-detail', args=(self.marinara.pk, ))
            ]
        })
        assert pizza_serializer.is_valid() is True

    def test_invalid_data(self):

        pizza_serializer = PizzaSerializer(data={
            'name': 'Pepperoni',
            'price': 'a',
            'toppings': [
                reverse('topping-detail', args=(self.pepperoni.pk, )),
            ]
        })
        assert pizza_serializer.is_valid() is False
        assert str(pizza_serializer.errors['price'][0]) == 'A valid number is required.'
        assert [str(err) for err in pizza_serializer.errors['toppings']] == ['No sauce, please add some sauce.', 'No cheese, please add some cheese.']

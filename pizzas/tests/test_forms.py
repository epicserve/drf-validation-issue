from pizzas.forms import PizzaForm
from pizzas.tests.test_base import BasePizzaTest


class TestPizzaForm(BasePizzaTest):

    def setUp(self):
        self.create_toppings()

    def test_valid_data(self):
        pizza_form = PizzaForm(data={
            'name': 'Pepperoni',
            'price': '12.99',
            'toppings': [self.pepperoni.pk, self.mozzarella.pk, self.marinara.pk]
        })
        assert pizza_form.is_valid() is True

    def test_invalid_data(self):
        pizza_form = PizzaForm(data={
            'name': 'Pepperoni',
            'price': 'a',
            'toppings': [self.pepperoni.pk]
        })
        assert pizza_form.is_valid() is False
        assert pizza_form.errors['price'][0] == 'Enter a number.'
        assert pizza_form.errors['toppings'] == ['No sauce, please add some sauce.', 'No cheese, please add some cheese.']

import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS

from pizzas.models import Crust, Topping, ToppingType

cheese_list = [
    'Cheddar',
    'Colby',
    'Goat Cheese',
    'Monterey Jack',
    'Mozzarella',
    'Provolone',
]

sauce_list = [
    'Marinara',
    'Alfredo',
    'BBQ',
]

crust_list = [
    'Thin',
    'Original',
    'Pan'
]

meat_list = [
    'Bacon',
    'BBQ Chicken',
    'Beef',
    'Cajun Chicken',
    'Chicken',
    'Ham',
    'Meatballs',
    'Pepperoni',
    'Proscuitto',
    'Salami',
    'Sausage',
    'Turkey',
]

sea_food_list = [
    'Anchovies',
    'Cajun Prawn',
    'Crayfish',
    'Lobster',
    'Oysters',
    'Prawns',
    'Salmon',
    'Shrimps',
    'Smoked Salmon',
    'Squid',
    'Tuna',
    'Whitebait',
]

vegetable_list = [
    'Black Beans',
    'Broccoli',
    'Carrot',
    'Green Peppers',
    'Lettuce',
    'Mushrooms',
    'Onions',
    'Olives',
    'Red Beans',
    'Red Onions',
    'Red Peppers',
    'Roasted Cauliflower',
    'Roasted Garlic',
    'Roasted Peppers',
    'Snow Peas',
    'Spinach',
    'Sun Dried Tomatoes',
    'Sweet Corn',
]

topping_types = [
    {'name': 'Cheese', 'slug': 'cheese', 'list': cheese_list},
    {'name': 'Sauce', 'slug': 'sauce', 'list': sauce_list},
    {'name': 'Meat', 'slug': 'meat', 'list': meat_list},
    {'name': 'Sea Food', 'slug': 'sea-food', 'list': sea_food_list},
    {'name': 'Vegetable', 'slug': 'vegetable', 'list': vegetable_list},
]


def add_toppings(topping_list, topping_type):
    for topping_name in topping_list:
        Topping.objects.create(name=topping_name, type=topping_type)


class Command(BaseCommand):
    help = 'Load initial pizza toppings'

    def msg(self, s=''):
        self.stdout.write(self.style.SUCCESS(s))

    def handle(self, *args, **options):

        self.msg()
        self.msg('Loading initial data ...')
        self.msg()

        for crust in crust_list:
            Crust.objects.create(name=crust, slug=crust.lower())

        self.stdout.write(self.style.SUCCESS('Crusts added.'))

        for topping in topping_types:
            add_toppings(topping['list'], ToppingType.objects.create(name=topping['name'], slug=topping['slug']))

        self.stdout.write(self.style.SUCCESS('Toppings added.'))

        username = 'pizzaadmin'
        random_password = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789%^&*-_=+') for _ in range(8))
        get_user_model()._default_manager.db_manager(DEFAULT_DB_ALIAS).create_superuser(**{
            'username': username,
            'password': random_password,
        })

        self.msg()
        self.msg("You're ready to start making pizzas!")
        self.msg()
        self.msg(f'Login with the username, "{username}" and the password, "{random_password}".')
